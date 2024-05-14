from flasgger import Swagger


def init_swagger(app):
    swagger_template = {
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT authorization header using the Bearer scheme. Example: 'Bearer {token}'"
            }
        },
        "security": [{"BearerAuth": []}]
    }
    Swagger(app, parse=True, template=swagger_template)
