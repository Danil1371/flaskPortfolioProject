from app.resources import *
from app.resources.admin_panel import admin_route


def initialize_routes(app):
    def route(url, obj):
        return app.add_url_rule(url, view_func=obj.as_view(url))

    route('/', Index)
    route('/register', RegisterApi)
    route('/login', LoginApi)
    route('/logout', LogoutApi)
    route('/profile', ProfileApi)
    route('/profile/avatar', SetAvatarProfileApi)
    route('/users', UsersApi)

    admin_route(app)
