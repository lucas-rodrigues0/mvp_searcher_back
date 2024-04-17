from sqlalchemy import Column, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid


from model import Base


class Accounts(Base):
    __tablename__ = "accounts"

    account_id = Column(
        "account_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username = Column(String(50), nullable=False)
    email = Column(String(50), unique=True)
    password = Column(String(20), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    def __init__(self, username: str, email: str, password: str):
        self.username = username
        self.email = email
        self.password = password
