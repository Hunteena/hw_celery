import flask

error_bp = flask.Blueprint('error_bp', __name__)


class HTTPError(Exception):
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message


@error_bp.app_errorhandler(HTTPError)
def handle_http_error(error):
    response = flask.jsonify({'message': error.message})
    response.status_code = error.status_code
    return response
