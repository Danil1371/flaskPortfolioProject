import os
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_openapi3 import OpenAPI
from app.db import init_engine, session
from app.tools.custom_exceptions import app_exceptions
from app.tools.logs import logger_config
from app.tools.swagger import init_swagger


jwt = JWTManager()
cors = CORS(resources={r"/*": {"origins": "*"}})

from app.db.models import *


logger_config()


def create_app(test_config=None):
    from app.resources.routes import initialize_routes

    enable_openapi_doc = os.getenv("FLASK_CONFIG") != "ProdConfig"
    app = OpenAPI(__name__, doc_ui=enable_openapi_doc)

    init_swagger(app)

    if test_config is None:
        app.config.from_object('config.' + os.environ['FLASK_CONFIG'])
    else:
        app.config.update(test_config)

    jwt.init_app(app)
    cors.init_app(app)

    initialize_routes(app)
    init_engine(app.config['SQLALCHEMY_DATABASE_URI'])

    @app.teardown_request
    def session_clear(exception=None):
        session.remove()
        if exception and session.is_active:
            session.rollback()

    app_exceptions(app, __name__)

    return app
