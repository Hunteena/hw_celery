import flask
import pydantic
from flask.views import MethodView

from auth import check_token
from db_models import Session, AdvModel
from errors import HTTPError
from validators import CreateAdvValidator

advs_bp = flask.Blueprint('advs_bp', __name__)


class AdvView(MethodView):
    def get(self, adv_id):
        with Session() as session:
            advs = session.query(AdvModel)
            if adv_id is None:
                return flask.jsonify([
                    adv.to_dict()
                    for adv in advs.order_by(AdvModel.id).all()
                ])
            adv = advs.filter(AdvModel.id == adv_id).first()
        if adv is None:
            raise HTTPError(404, f'no adv with id {adv_id}')
        return flask.jsonify(adv.to_dict())

    def post(self):
        with Session() as session:
            token = check_token(session)
            if not token:
                raise HTTPError(403, 'auth error')

            new_adv_data = flask.request.json
            try:
                validated_data = CreateAdvValidator(**new_adv_data).dict()
            except pydantic.ValidationError as er:
                raise HTTPError(400, er.errors())

            new_adv = AdvModel(
                title=validated_data['title'],
                description=validated_data['description'],
                owner_id=token.user_id
            )
            session.add(new_adv)
            session.commit()
            response = flask.jsonify(new_adv.to_dict())
            response.status_code = 201
            return response

    def delete(self, adv_id):
        with Session() as session:
            adv = session.query(AdvModel).filter(AdvModel.id == adv_id).first()
            if adv is None:
                raise HTTPError(404, f'no adv with id {adv_id}')
            if adv.owner.email != flask.request.headers.get('email'):
                raise HTTPError(401, 'auth err')
            session.delete(adv)
            session.commit()
            return flask.jsonify({'message': f'adv {adv_id} deleted'})

    def patch(self, adv_id):
        with Session() as session:
            query = session.query(AdvModel).filter(AdvModel.id == adv_id)
            adv = query.first()
            if adv is None:
                raise HTTPError(404, f'no adv with id {adv_id}')
            if adv.owner.email != flask.request.headers.get('email'):
                raise HTTPError(401, 'auth err')
            query.update(flask.request.json)
            session.commit()
            return flask.jsonify(adv.to_dict())


advs_bp.add_url_rule(
    '/', view_func=AdvView.as_view('get_all_adv'), methods=['GET'],
    defaults={'adv_id': None}
)
advs_bp.add_url_rule(
    '/<int:adv_id>/', view_func=AdvView.as_view('get_adv'), methods=['GET']
)
advs_bp.add_url_rule(
    '/', view_func=AdvView.as_view('create_adv'), methods=['POST']
)
advs_bp.add_url_rule(
    '/<int:adv_id>/', view_func=AdvView.as_view('delete_adv'),
    methods=['DELETE']
)
advs_bp.add_url_rule(
    '/<int:adv_id>/', view_func=AdvView.as_view('update_adv'),
    methods=['PATCH']
)
