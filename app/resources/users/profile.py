from werkzeug.exceptions import BadRequest
from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity
from pydantic import BaseModel, field_validator
from typing import Optional
from app.db import session
from app.db.models.user import UserModel, UserResponseModel
from app.db.models.language import AppLanguageModel
from app.tools.schemas import documentation, DefaultResponseModel
from app.tools.tokens import custom_token_required
from app.helpers.file_utils import upload_image, delete_image


class EditProfileSchema(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    app_language: Optional[str] = None

    @field_validator('app_language')
    def check_app_language(cls, v):
        if v and not session.query(AppLanguageModel).filter_by(name=v).first():
            raise BadRequest(f"Value {v} is not in the list of available")
        return v


class ProfileApi(MethodView):
    @staticmethod
    @documentation(
        tags=["Profile"],
        description="Get Profile",
        response_model=UserResponseModel,
    )
    @custom_token_required(['user', 'moderator'])
    def get():
        curr_user = session.query(UserModel).get(get_jwt_identity())
        if not curr_user:
            return {"error": "bad token"}, 401
        return UserResponseModel(**curr_user.to_json()).model_dump()

    @staticmethod
    @documentation(
        tags=["Profile"],
        description="Edit Profile",
        request_model=EditProfileSchema,
        data_type="body",
    )
    @custom_token_required(['user', 'moderator'])
    def patch():
        data = EditProfileSchema(**request.get_json()).model_dump(exclude_unset=True)
        curr_user = session.query(UserModel).get(get_jwt_identity())
        if not curr_user:
            return {"error": "bad token"}, 401

        for field in data:
            setattr(curr_user, field, data[field])

        session.commit()
        return DefaultResponseModel().model_dump()

    @staticmethod
    @documentation(
        tags=["Profile"],
        description="Delete User",
    )
    @custom_token_required(['user', 'moderator'])
    def delete():
        curr_user = session.query(UserModel).get(get_jwt_identity())
        if not curr_user:
            return {"error": "bad token"}, 401

        delete_image(curr_user.avatar)

        session.delete(curr_user)
        session.commit()
        return DefaultResponseModel().model_dump()


class SetAvatarProfileApi(MethodView):
    @staticmethod
    @documentation(
        tags=["Profile"],
        description="Set An Avatar To Profile",
        file_name="avatar"
    )
    @custom_token_required(['user', 'moderator'])
    def patch():
        avatar = request.files.get('avatar')

        curr_user = session.query(UserModel).get(get_jwt_identity())
        if not curr_user:
            return {"error": "bad token"}, 401

        if avatar:
            delete_image(curr_user.avatar)
            curr_user.avatar = upload_image(avatar, "/static/test_avatars/")

        session.commit()
        return DefaultResponseModel().model_dump()
