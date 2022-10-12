import flask
from flask.views import MethodView
from celery.result import AsyncResult

from db_models import Session, UserModel
from errors import HTTPError
from tasks import send_mails

mailing_bp = flask.Blueprint('mailing_bp', __name__)


class MailingListView(MethodView):
    def get(self, task_id):
        task = AsyncResult(task_id)
        return flask.jsonify({'status': task.status,
                              'result': task.result})

    def post(self):
        try:
            email_body = flask.request.json['body']
        except KeyError as er:
            print(f'{er} is required')
            raise HTTPError(400, f'{er} is required')
        with Session() as session:
            # TODO split users in chunks
            users = session.query(UserModel).all()
            emails = [user.email for user in users]
        task = send_mails.delay(email_body, emails)
        return flask.jsonify({'task_id': task.id})


mailing_bp.add_url_rule(
    '/<task_id>/', view_func=MailingListView.as_view('get_task_status'),
    methods=['GET']
)
mailing_bp.add_url_rule(
    '/', view_func=MailingListView.as_view('send_emails'), methods=['POST']
)
