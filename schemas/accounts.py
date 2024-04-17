from datetime import datetime
from pydantic import BaseModel


class AccountSchema(BaseModel):
    """Define como um novo usuário será representado para inserção na base de dados"""

    username: str = "Nome Usuario"
    email: str = "novo@mail.com"
    password: str = "123456"


class AccountAuthForm(BaseModel):
    """Define como um usuário já cadastrado será representado para a autenticação"""

    email: str = "novo@mail.com"
    password: str = "123456"


class AccountToken(BaseModel):
    """Define como será o retorno da autenticação de usuário existente"""

    account_id: str
    token: str
