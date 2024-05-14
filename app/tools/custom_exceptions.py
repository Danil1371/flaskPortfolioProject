import traceback
from werkzeug.exceptions import BadRequest, Unauthorized, Forbidden, NotFound, HTTPException
from flask import jsonify
from pydantic import ValidationError
from app.tools.logs import get_logger


def app_exceptions(app, logger_name):
    logger = get_logger(logger_name)

    @app.errorhandler(BadRequest)
    def handle_400_error(e):
        logger.warning(f"Bad Request: {str(e)}")
        return jsonify({"error": str(e).replace("400 Bad Request: ", "")}), 400

    @app.errorhandler(ValidationError)
    def handle_400_error(e):
        logger.warning(f"Validation Error: {e.errors()}")
        return jsonify({"error": e.errors()}), 400

    @app.errorhandler(Unauthorized)
    def handle_401_error(e):
        logger.warning(f"Unauthorized: {str(e)}")
        return jsonify({"error": "Unauthorized"}), 401

    @app.errorhandler(Forbidden)
    def handle_403_error(e):
        logger.warning(f"Forbidden: {str(e)}")
        return jsonify({"error": "Forbidden"}), 403

    @app.errorhandler(NotFound)
    def handle_404_error(e):
        logger.warning(f"Not Found: {str(e)}")
        return jsonify({"error": "Not Found"}), 404

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return e
        traceback.print_exc()
        logger.warning(f"Unhandled Exception: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500
