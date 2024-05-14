from datetime import datetime
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from sqlalchemy.orm.exc import StaleDataError
from app import jwt
from app.db import session
from app.db.models import TokenBlockListModel, UserModel


@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = session.query(TokenBlockListModel).filter_by(jti=jti).scalar()
    return token is not None


def custom_token_required(roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if claims["role"] in roles:
                try:
                    session.bulk_update_mappings(UserModel, [{"id": claims.get("sub"), "last_online": datetime.utcnow()}])
                    session.commit()
                except StaleDataError:
                    return {"error": "Bad token"}, 401
                return fn(*args, **kwargs)
            else:
                return {"error": "Bad token"}, 403
        return decorator

    return wrapper
