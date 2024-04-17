import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv

# importando os elementos definidos no modelo
from model.base import Base
from model.accounts import Accounts
from model.comments import Comments
from model.pdf_pages import PdfPages


load_dotenv(override=True)

config = {
    "dbname": os.getenv("DATABASE"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
}

# # cria a engine de conexão com o banco
# dialect+driver://username:password@host:port/database
postgres_url = f"postgresql+psycopg2://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['dbname']}"

engine = create_engine(postgres_url)

# cria o database caso não exista
if not database_exists(engine.url):
    create_database(engine.url)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)
