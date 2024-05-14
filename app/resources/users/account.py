from flask import request
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from pydantic import BaseModel, EmailStr
from app.db import session
from app.db.models import UserModel, TokenBlockListModel
from app.tools.schemas import documentation, DefaultResponseModel


class AccountSchema(BaseModel):
    email: EmailStr
    password: str


class AccountResponseModel(BaseModel):
    access_token: str


class RegisterApi(MethodView):
    @staticmethod
    @documentation(
        tags=["Account"],
        description="Register",
        request_model=AccountSchema,
        response_model=AccountResponseModel,
        data_type="body",
    )
    def post():
        data = AccountSchema(**request.get_json()).model_dump()

        if session.query(UserModel).filter_by(email=data['email']).first():
            return {"error": f"User with email {data['email']} already exists."}, 400

        new_user = UserModel(
            email=data['email'],
            app_language='English'
        )
        new_user.set_password(data['password'])
        session.add(new_user)
        session.flush()
        new_user.first_name = 'user'
        new_user.last_name = f'ID{new_user.id}'

        access_token = create_access_token(new_user.id, expires_delta=False,
                                           additional_claims={'role': str(new_user.role)})
        session.commit()
        return AccountResponseModel(**{'access_token': access_token}).model_dump()


class LoginApi(MethodView):
    @staticmethod
    @documentation(
        tags=["Account"],
        description="Login",
        request_model=AccountSchema,
        response_model=AccountResponseModel,
        data_type="body",
    )
    def post():
        data = AccountSchema(**request.get_json()).model_dump()
        user = session.query(UserModel).filter(UserModel.email == data['email']).first()
        if not user or not user.check_password(data['password']):
            return {'error': 'Incorrect password or email'}, 400
        access_token = create_access_token(user.id,
                                           expires_delta=False,
                                           additional_claims={'role': str(user.role)})
        return AccountResponseModel(**{'access_token': access_token}).model_dump()


class LogoutApi(MethodView):
    @staticmethod
    @documentation(
        tags=["Account"],
        description="Logout",
    )
    @jwt_required()
    def post():
        jti = get_jwt()["jti"]
        session.add(TokenBlockListModel(jti=jti))
        session.commit()
        return DefaultResponseModel().model_dump()
