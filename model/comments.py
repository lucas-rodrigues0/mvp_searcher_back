from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

from model import Base


class Comments(Base):
    __tablename__ = "comments"

    comment_id = Column(
        "comment_id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    content = Column(String(350), nullable=False)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    account_id = Column(
        UUID(as_uuid=True), ForeignKey("accounts.account_id"), nullable=False
    )

    def __init__(self, content: str, account_id):
        self.content = content
        self.account_id = account_id
