from pydantic import BaseModel
from typing import List

from model import Accounts, Comments


class CommentSchema(BaseModel):
    """Define como um novo comentario será representado para inserção na base de dados"""

    content: str


class CommentViewSchema(BaseModel):
    """Define como será retornado o novo comentário inserido na base"""

    comment_id: str = "b36a2227-8db8-449c-b9ca-889f3f89787d"
    account_id: str = "2a2e4d1a-8db4-4f78-8f1e-5393f3285431"
    username: str = "Nome do usuário"
    content: str = "qualquer texto de comentario"
    created_at: str = "06/04/2024"


class CommentsListSchema(BaseModel):
    """Define como será o retorno para todos os comentários existentes na base"""

    comments: List[CommentViewSchema]


def serialize_comments_list(comments: List[tuple[Comments, Accounts]]):
    """Retorna uma representação de todos os comentários salvos na base
    seguindo a definição no CommentViewSchema
    """
    result = []
    for comment, account in comments:
        result.append(
            {
                "comment_id": comment.comment_id,
                "account_id": comment.account_id,
                "username": account.username,
                "content": comment.content,
                "created_at": comment.created_at.strftime("%d/%m/%Y"),
            }
        )
    return {"comments": result}
