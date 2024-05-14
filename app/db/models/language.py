from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.db.models import Base


class AppLanguageModel(Base):
    __tablename__ = 'app_languages'
    name = Column(String(50), primary_key=True)
    users = relationship('UserModel', backref='app_language_model')
