import warnings
from werkzeug.exceptions import HTTPException
from flask import redirect, Response
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_basicauth import BasicAuth
from app.db import session
from app.db.models import UserModel


def admin_route(app):
    basic_auth = BasicAuth(app)

    class DashboardView(AdminIndexView):
        def is_visible(self):
            return False

    class AuthException(HTTPException):
        def __init__(self, message):
            super().__init__(message, Response(
                message, 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))

    class AdminView(ModelView):
        can_create = False
        can_delete = False

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def is_accessible(self):
            if not basic_auth.authenticate():
                raise AuthException('Not authenticated. Refresh the page.')
            else:
                return True

        def inaccessible_callback(self, name, **kwargs):
            return redirect(basic_auth.challenge())

    class UserView(AdminView):
        column_list = ['id', 'role', 'email', 'full_name', 'verified', 'created_at', 'app_language', 'last_online']
        column_filters = ['role', 'email', 'full_name']
        form_edit_rules = ('role', 'verified')

    admin = Admin(app, name='FlaskPortfolioProject', index_view=DashboardView())
    with warnings.catch_warnings():
        warnings.filterwarnings('ignore', 'Fields missing from ruleset', UserWarning)
        admin.add_view(UserView(UserModel, session, 'Users'))
