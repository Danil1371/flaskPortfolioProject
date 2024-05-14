from flask.views import MethodView


class Index(MethodView):
    @staticmethod
    def get():
        return {"msg": "ok"}
