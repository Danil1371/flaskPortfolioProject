from datetime import datetime
from sqlalchemy import Column, String, DateTime
from app.db.models import Base


class TokenBlockListModel(Base):
    __tablename__ = 'tokens_block_list'
    jti = Column(String(50), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
