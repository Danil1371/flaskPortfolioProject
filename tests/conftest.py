import logging
import pytest
import os
from dotenv import load_dotenv
from flask_jwt_extended import create_access_token
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from app import create_app
from app.db.models import UserModel, AppLanguageModel, TokenBlockListModel
from app.db.seeds import create_seeds

load_dotenv()

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

DATABASE_CONNECTION_URI = "postgresql+psycopg2:///flask_portfolio_project_test"

db_tables = [UserModel.__table__, AppLanguageModel.__table__, TokenBlockListModel.__table__]


@pytest.fixture(scope="session")
def app():
    logger.info("APP")
    app = create_app(test_config={
        "SQLALCHEMY_DATABASE_URI": DATABASE_CONNECTION_URI,
        "JWT_SECRET_KEY": os.environ.get("JWT_SECRET_KEY"),
        "PASSWORD_SALT": os.environ.get("PASSWORD_SALT")
    })
    with app.app_context():
        yield app


@pytest.fixture(scope="session")
def db_session(app):
    logger.info("DB SESSION")
    engine = create_engine(DATABASE_CONNECTION_URI)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    metadata = MetaData()
    metadata.create_all(bind=engine, tables=db_tables)
    create_seeds(app, session)
    session.commit()

    yield session

    logger.info("CLOSE DB SESSION")
    session.rollback()
    session.close()
    metadata.drop_all(bind=engine, tables=db_tables)
    engine.dispose()


@pytest.fixture(scope="session")
def access_headers(db_session):
    user = UserModel(role='moderator')
    db_session.add(user)
    db_session.commit()

    access_token = create_access_token(
        user.id,
        expires_delta=False,
        additional_claims={'role': str(user.role)}
    )
    yield {
        'Authorization': f'Bearer {access_token}'
    }

    db_session.delete(user)
    db_session.commit()


@pytest.fixture(scope="session")
def client(app, db_session):
    logger.info("CLIENT")
    with app.test_client() as client:
        yield client
