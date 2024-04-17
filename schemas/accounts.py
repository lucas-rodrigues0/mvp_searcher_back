from datetime import datetime
from pydantic import BaseModel


class AccountSchema(BaseModel):
    """Define como um novo usuário será representado para inserção na base de dados"""

    username: str
    email: str
    password: str


class AccountAuthForm(BaseModel):
    """Define como um usuário já cadastrado será representado para a autenticação"""

    email: str
    password: str


class AccountToken(BaseModel):
    """Define como será o retorno da autenticação de usuário existente"""

    account_id: str
    token: str
