from app.db import session
from app.db.models import *


def app_languages(session_):
    for elem in ['English', 'Spanish']:
        session_.add(AppLanguageModel(name=elem))


def create_seeds(app_, session_):
    with app_.app_context():
        app_languages(session_)


if __name__ == '__main__':
    from application import app

    create_seeds(app, session)
    session.commit()
