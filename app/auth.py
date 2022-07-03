import flask
from flask.views import MethodView

import pydantic

from db_models import Session, UserModel, Token
from errors import HTTPError
from validators import CreateUserValidator

auth_bp = flask.Blueprint('auth_bp', __name__)


def check_token(session):
    token = (
        session.query(Token).join(UserModel).filter(
            UserModel.email == flask.request.headers.get('email'),
            Token.id == flask.request.headers.get('token')
        ).first()
    )
    if token is None:
        raise HTTPError(401, 'invalid token')
    return token


class UserView(MethodView):
    def get(self, user_id: int):
        with Session() as session:
            token = check_token(session)
            if token.user.id != user_id:
                raise HTTPError(403, 'auth error')
            return flask.jsonify((token.user.to_dict()))

    def post(self):
        new_user_data = flask.request.json

        try:
            validated_data = CreateUserValidator(**new_user_data).dict()
        except pydantic.ValidationError as er:
            raise HTTPError(400, er.errors())

        with Session() as session:
            new_user = UserModel.register(session, **validated_data)
            response = flask.jsonify(new_user.to_dict())
            response.status_code = 201
            return response


@auth_bp.route("/login/", methods=['POST'])
def login():
    login_data = flask.request.json
    with Session() as session:
        user = (
            session.query(UserModel).filter(
                UserModel.email == login_data['email']
            ).first()
        )
        if user is None or not user.check_password(login_data['password']):
            raise HTTPError(401, 'incorrect user or password')
        token = Token(user_id=user.id)
        session.add(token)
        session.commit()
        return flask.jsonify({'token': token.id})


auth_bp.add_url_rule(
    "/user/", view_func=UserView.as_view("register_user"), methods=["POST"]
)
auth_bp.add_url_rule(
    "/user/<int:user_id>/", view_func=UserView.as_view("view_user"),
    methods=["GET"]
)
