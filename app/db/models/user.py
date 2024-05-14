import re
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import BadRequest
from flask import current_app
from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey, Boolean
from sqlalchemy.ext.hybrid import hybrid_property
from pydantic import BaseModel
from typing import Optional
from app.db.models import Base
from app.helpers.file_utils import get_image


class UserModel(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    email = Column(String(255), unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    avatar = Column(String(255), unique=True)
    role = Column(Enum('user', 'moderator', name='user_role'), default='user')
    verified = Column(Boolean, default=False)
    app_language = Column(String(50), ForeignKey('app_languages.name'))
    last_online = Column(DateTime, default=datetime.utcnow)
    password_hash = Column(String(255))

    def set_password(self, password):
        if not re.match(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$", password):
            raise BadRequest(
                "Password must contain at least one digit, one lowercase and one uppercase letter, "
                "and be at least 8 characters long."
            )
        self.password_hash = generate_password_hash(password + current_app.config['PASSWORD_SALT'])

    def check_password(self, password):
        return check_password_hash(self.password_hash, password + current_app.config['PASSWORD_SALT'])

    @hybrid_property
    def full_name(self):
        return self.first_name + ' ' + self.last_name if self.first_name and self.last_name else self.first_name if self.first_name else None

    def to_json(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'avatar': get_image(self.avatar),
            'role': self.role,
            'verified': self.verified,
            'app_language': self.app_language,
            'last_online': self.last_online.strftime('%H:%M %d/%m/%Y (UTC)') if self.last_online else None
        }

    def __repr__(self):
        return '<UserModel {}>'.format(self.id)


class UserResponseModel(BaseModel):
    id: int
    full_name: Optional[str] = None
    email: str
    avatar: Optional[str] = None
    role: Optional[str] = None
    verified: Optional[bool] = None
    app_language: Optional[str] = None
    last_online: Optional[str] = None
