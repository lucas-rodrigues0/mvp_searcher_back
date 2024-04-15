import jwt
import os
from dotenv import load_dotenv


load_dotenv(override=True)

JWT_SECRET = os.getenv("JWT_SECRET")


def jwt_encode(payload_data):
    """Codifica o payload em um token JWT"""
    return jwt.encode(payload=payload_data, key=JWT_SECRET)


def jwt_decode(token):
    """Tenta decodificar um token para a validação do usuário"""
    try:
        header_data = jwt.get_unverified_header(token)

        return jwt.decode(token, key=JWT_SECRET, algorithms=[header_data["alg"]])
    except jwt.exceptions.DecodeError:
        return False
