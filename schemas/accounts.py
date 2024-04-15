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


class AccountViewSchema(BaseModel):
    """Define como será o retorno para novo usuário inserido na base de dados"""

    account_id: str = "b086db2f-2cbd-4e5d-975d-1567a4db1b95"
    username: str = "Nome do Usuario"
    email: str = "email@mail.com"
    active: bool = True
    updated_at: datetime = "05/04/2024"


class AccountToken(BaseModel):
    """Define como será o retorno da autenticação de usuário existente"""

    account_id: str
    token: str
