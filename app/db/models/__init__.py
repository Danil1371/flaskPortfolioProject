from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from app.db.models.user import UserModel
from app.db.models.language import AppLanguageModel
from app.db.models.tokens_block_list import TokenBlockListModel
