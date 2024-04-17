from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime

from model import Base


class PdfPages(Base):
    __tablename__ = "pdf_pages"

    page_num = Column(Integer, primary_key=True)
    titulo_num = Column(String(15), nullable=True)
    capitulo_num = Column(String(15), nullable=True)
    page_content = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())

    def __init__(self, page_num: int, page_content: str):
        self.page_num = page_num
        self.page_content = page_content
