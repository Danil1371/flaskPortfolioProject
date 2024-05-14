from flask import request
from flask.views import MethodView
from sqlalchemy import or_
from paginate_sqlalchemy import SqlalchemyOrmPage
from pydantic import BaseModel, Field
from typing import Optional, List
from app.db.models import UserModel
from app.db import session
from app.tools.schemas import documentation, PaginationSchema
from app.tools.tokens import custom_token_required


class UsersSchema(PaginationSchema):
    search: Optional[str] = ""
    sort_by: Optional[str] = Field(enum=["name", "email", "id", "created_at"], default="created_at")
    sort_order: Optional[str] = Field(enum=["asc", "desc"], default="desc")


class UsersResponseModel(BaseModel):
    items: List = []
    total: int = 0


class UsersApi(MethodView):
    @staticmethod
    @documentation(
        tags=["Users"],
        description="Users List",
        request_model=UsersSchema,
        response_model=UsersResponseModel,
        data_type="query",
    )
    @custom_token_required(['moderator'])
    def get():
        data = UsersSchema(**request.args.to_dict()).model_dump()

        users = session.query(UserModel)

        if data.get('search'):
            users = users.filter(or_(
                UserModel.email.ilike(f'%{data["search"]}%'),
                UserModel.full_name.ilike(f'%{data["search"]}%')
            ))

        if data.get('sort_by') == 'name':
            sort_by = UserModel.full_name
        elif data.get('sort_by') == 'email':
            sort_by = UserModel.email
        elif data.get('sort_by') == 'id':
            sort_by = UserModel.id
        else:
            sort_by = UserModel.created_at

        if data.get('sort_order') == 'desc':
            users = users.order_by(sort_by.desc())
        else:
            users = users.order_by(sort_by.asc())

        users = SqlalchemyOrmPage(users, page=data['page'], items_per_page=data['per_page'])
        result = {"items": [user.to_json() for user in users.items], "total": users.item_count}
        return UsersResponseModel(**result).model_dump()
