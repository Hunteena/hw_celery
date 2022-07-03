import os

import flask

from celery import Celery


def make_celery(app):

    celery = Celery(app.import_name, include=['tasks'])
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = flask.Flask('app')
broker = os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/5')
backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6379/6')

flask_app.config.update(CELERY_CONFIG={
    'broker_url': broker,
    'result_backend': backend,
})
celery_app = make_celery(flask_app)
celery_app.set_default()
