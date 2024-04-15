import os
from dotenv import load_dotenv


load_dotenv(override=True)

def load_config():
    config = {
        "dbname": os.getenv("DATABASE"),
        "user": os.getenv("USER"),
        "password": os.getenv("PASSWORD"),
        "host": os.getenv("HOST"),
        "port": os.getenv("PORT")
    }

    return config
