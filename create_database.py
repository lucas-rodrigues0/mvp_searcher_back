from model import engine, Base, Session, Accounts, Comments


def create_database():
    print("Droping old tables")
    Base.metadata.drop_all(
        engine,
        tables=[
            Base.metadata.tables["accounts"],
            Base.metadata.tables["comments"],
            Base.metadata.tables["pdf_pages"],
        ],
    )

    print("Creating new tables")
    Base.metadata.create_all(engine)

    session = Session()

    account1 = Accounts(
        username="Meu Nome",
        email="email@mail.com",
        password="123",
    )

    account2 = Accounts(
        username="Eu",
        email="myemail@mail.com",
        password="123456",
    )

    print("Adding accounts")
    session.add(account1)
    session.add(account2)

    session.flush()
    print("Session flushed")

    comment1 = Comments(
        account_id=account1.account_id,
        content="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
    )
    comment2 = Comments(
        account_id=account2.account_id,
        content="Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
    )
    print("Adding comments")
    session.add(comment1)
    session.add(comment2)

    print("Commiting")
    session.commit()
    session.close()

    print("Closed session")
    return


if __name__ == "__main__":
    create_database()
