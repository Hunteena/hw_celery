from flask_celery import flask_app

from advs import advs_bp
from auth import auth_bp
from errors import error_bp
from mailing_list import mailing_bp

flask_app.register_blueprint(error_bp)
flask_app.register_blueprint(advs_bp)
flask_app.register_blueprint(auth_bp)
flask_app.register_blueprint(mailing_bp, url_prefix='/mailing')

if __name__ == '__main__':
    flask_app.run()
