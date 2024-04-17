from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect, request

from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc

from auth import jwt_decode, jwt_encode
from model import Session, Accounts, Comments
from full_text_searcher.searcher import query_full_text_searcher
from logger import logger
from schemas import *
from flask_cors import CORS


info = Info(title="CF searcher API", version="1.0.0")
jwt_schema = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
security_schemes = {"jwt": jwt_schema}
app = OpenAPI(__name__, info=info, security_schemes=security_schemes)
CORS(app)

security = [{"jwt": []}]

home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
account_tag = Tag(
    name="Accounts", description="Autenticação e adição de usuarios (account) à base"
)
comment_tag = Tag(
    name="Comments",
    description="Listagem dos comentários existentes e adição de um novo, por um usuário cadastrado na base",
)
searcher_tag = Tag(
    name="Searcher",
    description="Busca por termos existentes no conteúdo de PDF com técnica de full-text search",
)


@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


@app.post(
    "/account/register",
    tags=[account_tag],
    responses={"200": AccountToken, "409": ErrorSchema, "400": ErrorSchema},
)
def register_account(body: AccountSchema):
    """Adiciona um novo Usuário à base de dados
    Retorna uma representação do usuário definido no schema.
    """
    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        error_msg = "Nome de usuário e senha são necessários para registro"
        logger.warning(f"Erro ao adicionar usuario. {error_msg}")
        return {"data": {"message": error_msg}}, 409

    account = Accounts(username=username, email=email, password=password)
    logger.debug(f"Adicionando usuario de nome: '{account.username}'")

    try:
        session = Session()
        session.add(account)
        session.commit()
        data = {
            "account_id": str(account.account_id),
            "username": account.username,
            "email": account.email,
        }

        logger.debug(f"Adicionado usuário de nome: '{account.username}'")

        # Usa os dados necessários do usuário para a codificação do token JWT
        token = jwt_encode(data)

        return {"data": {"token": token, "account_id": str(account.account_id)}}, 200

    except IntegrityError as e:
        error_msg = "Usuário de mesmo email já salvo na base"
        logger.warning(
            f"Erro ao adicionar usuario '{account.username} com o email {account.email}', {error_msg}"
        )
        return {"data": {"message": error_msg}}, 409

    except Exception as e:
        error_msg = "Não foi possível salvar novo item"
        logger.warning(f"Erro ao adicionar usuário '{account.username}', {error_msg}")
        return {"data": {"message": error_msg}}, 400


@app.post(
    "/account/login",
    tags=[account_tag],
    responses={"200": AccountToken, "403": ErrorSchema, "404": ErrorSchema},
)
def signin_account(body: AccountAuthForm):
    """Faz a busca do usuarios cadastrado e autentica o password"""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    logger.debug(f"Login de usuário com email: {email}")

    session = Session()
    account = session.query(Accounts).filter(Accounts.email == email).first()

    if not account:
        return {"data": {"message": "User not found by email"}}, 404
    elif password != account.password:
        return {"data": {"message": "Invalid password"}}, 403
    else:
        # Extrai os dados necessários do usuário para a codificação do token JWT
        encode_data = {
            "account_id": str(account.account_id),
            "username": account.username,
            "email": account.email,
        }
        token = jwt_encode(encode_data)

        return {"data": {"token": token, "account_id": str(account.account_id)}}, 200


@app.get("/comments", tags=[comment_tag], responses={"200": CommentsListSchema})
def get_all_comments():
    """Faz a busca por todos os comentários inseridos na base
    e retorna uma lista dos comentários como definido no schema"""

    logger.debug("Buscando comentários existentes")
    session = Session()

    comments = (
        session.query(Comments, Accounts)
        .filter(Comments.account_id == Accounts.account_id)
        .order_by(desc(Comments.created_at))
        .all()
    )

    if not comments:
        data = {"comments": []}
    else:
        logger.debug(f"%d comentarios encontrados" % len(comments))

        data = serialize_comments_list(comments)
    return {"data": data}, 200


@app.post(
    "/comments",
    tags=[comment_tag],
    responses={
        "200": CommentViewSchema,
        "400": ErrorSchema,
        "403": ErrorSchema,
        "409": ErrorSchema,
    },
    security=security,
)
def insert_comment(body: CommentSchema):
    """Adiciona um novo comentário à base de dados
    Retorna uma representação do novo comentário inserido na base.
    """
    logger.debug("Inserindo comentário")

    # Verifica o token passado no header
    token = str(request.authorization).split(" ")[-1]
    token_check = jwt_decode(token)

    if not token_check:
        error_msg = "Login não encontrado. É necessário estar logado para inserir novo comentário."
        logger.warning(f"Erro ao adicionar comentário. {error_msg}")
        return {"data": {"message": error_msg}}, 403

    data = request.get_json()
    account_id = token_check.get("account_id")
    content = data.get("content")

    if not content:
        error_msg = "Conteúdo necessário para inserir comentário."
        logger.warning(f"Erro ao adicionar comentário. {error_msg}")
        return {"data": {"message": error_msg}}, 409

    comment = Comments(account_id=account_id, content=content)
    logger.debug(f"Adicionando comentário de account com id: '{comment.account_id}'")

    try:
        session = Session()
        account = session.get_one(Accounts, account_id)
        session.add(comment)
        session.commit()

        data = {
            "comment_id": str(comment.comment_id),
            "account_id": str(comment.account_id),
            "account_username": account.username,
            "content": comment.content,
            "updated_at": str(comment.updated_at),
        }

        return {"data": data}, 200

    except Exception as e:
        error_msg = "Não foi possível inserir novo comentário"
        logger.warning(
            f"Erro ao adicionar comentário da account '{comment.account_id}', {error_msg}"
        )
        return {"data": {"message": error_msg}}, 400


@app.get(
    "/searcher",
    tags=[searcher_tag],
    responses={"200": SearcherResponseSchema, "403": ErrorSchema},
    security=security,
)
def query_searcher(query: SearcherQuerySchema):
    """Faz um full-text search dos termos, em conteúdo do PDF indexado.
    Retorna os resultados contendo as páginas em que forma encontrados os termos,
    assim como uma amostragem do conteúdo, onde cada termos foi encontrado.
    """

    token = str(request.authorization).split(" ")[-1]
    token_check = jwt_decode(token)

    if token_check:
        data = request.args
        query_param = data.get("query")
        results = query_full_text_searcher(query=query_param)

        return {"data": {"results": results, "total_count": len(results)}}, 200

    error_msg = "Autenticação necessária. Fazer o login antes de pesquisar."
    logger.warning(f"Erro a pesquisar. {error_msg}")
    return {"data": {"message": error_msg}}, 403


if __name__ == "__main__":
    app.run(debug=True)
