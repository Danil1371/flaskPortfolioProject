import os
from functools import wraps
from pydantic import BaseModel, Field
from typing import Optional
from flasgger import swag_from


class PaginationSchema(BaseModel):
    page: Optional[int] = 1
    per_page: Optional[int] = 20


class DefaultResponseModel(BaseModel):
    msg: str = Field("ok")


class DefaultErrorResponseModel(BaseModel):
    error: str


def documentation(
    tags,
    description=None,
    request_model=None,
    response_model=DefaultResponseModel,
    data_type=None,
    file_name=None
):
    parameters = []
    if request_model:
        required_params = request_model.schema().get("required") or []
        model_schema = request_model.schema().get("properties")
        if data_type == "body":
            body_schema = {}
            for item in model_schema:
                if model_schema[item].get('anyOf'):
                    body_schema.update({item: model_schema[item].get('anyOf')[0]})
                else:
                    body_schema.update({item: model_schema[item]})
            parameters.append(
                {
                    "in": data_type,
                    "name": "body",
                    "description": "Request body data",
                    "schema": {"type": "object", "properties": body_schema}
                }
            )
        elif data_type == "query":
            for name in model_schema:
                obj = {
                    "in": data_type,
                    "name": name,
                    "required": bool(name in required_params),
                    "description": "Request query data",
                    "schema": {"type": "string"},
                }
                if model_schema[name].get('enum'):
                    obj.update({"enum": model_schema[name].get('enum')})
                parameters.append(obj)
    if file_name:
        parameters.append(
            {
                "in": "formData",
                "name": file_name,
                "type": "string",
                "description": "The file to upload",
            }
        )

    def decorator(func):
        @swag_from(
            {
                "description": description,
                "tags": tags,
                "parameters": parameters,
                "consumes": ["application/json", "multipart/form-data"] if file_name else ["application/json"],
                "responses": {
                    200: {
                        "description": "Success",
                        "schema": {"type": "object", "properties": response_model.schema().get("properties")},
                    },
                    400: {
                        "description": "Bad Request",
                        "schema": {"type": "object", "properties": DefaultErrorResponseModel.schema().get("properties")}
                    },
                }
            }
            if os.getenv("FLASK_CONFIG") != "ProdConfig"
            else None
        )
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
