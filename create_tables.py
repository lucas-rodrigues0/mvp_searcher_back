from database.connection.db import Db


def create_tables():
    db = Db()

    command = """
    CREATE TABLE IF NOT EXISTS accounts (
        account_id UUID DEFAULT gen_random_uuid(),
        email VARCHAR(50) UNIQUE NOT NULL,
        username VARCHAR(50) NOT NULL,
        password VARCHAR(20) NOT NULL,
        active BOOLEAN NOT NULL DEFAULT TRUE,
        created_at DATE DEFAULT CURRENT_DATE,
        updated_at DATE DEFAULT CURRENT_DATE,
        PRIMARY KEY(account_id)
    );

    CREATE TABLE IF NOT EXISTS comments (
        comment_id UUID DEFAULT gen_random_uuid(),
        account_id UUID NOT NULL,
        content VARCHAR(350) NOT NULL,
        created_at DATE DEFAULT CURRENT_DATE,
        updated_at DATE DEFAULT CURRENT_DATE,
        PRIMARY KEY(comment_id),
        CONSTRAINT fk_account
            FOREIGN KEY(account_id) 
                REFERENCES accounts(account_id)
    );

    CREATE TABLE IF NOT EXISTS pdf_pages (
        page_num INTEGER,
        titulo_num VARCHAR(15),
        capitulo_num VARCHAR(15),
        page_content TEXT NOT NULL,
        created_at DATE DEFAULT CURRENT_DATE,
        updated_at DATE DEFAULT CURRENT_DATE,
        PRIMARY KEY(page_num)
    );
    """

    response = db.execute(command)
    print(response)


if __name__ == "__main__":
    create_tables()
