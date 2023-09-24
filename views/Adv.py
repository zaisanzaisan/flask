from flask import abort, jsonify, request
from flask.views import MethodView

from models import Advertisements, get_session
from validators import AdvValidate


class Adv(MethodView):
    def get(self):
        request_parameters = dict(request.json)
        session = get_session()
        if owner_id := request_parameters.get("owner_id"):
            db_resp = (
                session.query(Advertisements)
                .where(Advertisements.owner_id == owner_id)
                .all()
            )
        else:
            db_resp = session.query(Advertisements).all()
        context = dict()
        context["status"] = "ok"
        for cnt, adv in enumerate(db_resp):
            context[str(cnt)] = {  # am a great python developer 😂
                "id": adv.id,
                "owner_id": adv.owner_id,
                "title": adv.title,
                "description": adv.description,
            }
        context = jsonify(context)
        return context

    def post(self):
        validated_data = AdvValidate(**request.json).dict()
        session = get_session()
        adv = Advertisements(
            title=validated_data["title"],
            description=validated_data["description"],
            owner_id=validated_data["owner_id"],
        )
        session.add(adv)
        session.commit()
        # session.close()
        context = jsonify(
            {"status": "ok", "adv_id": adv.id, "created_at": adv.created_at}
        )
        return context

    def patch(self):
        pass

    def delete(self):
        validated_data = AdvValidate(**request.json).dict()
        session = get_session()
        i = (
            session.query(Advertisements)
            .filter(Advertisements.id == validated_data["id"])
            .filter(Advertisements.owner_id == validated_data["owner_id"])
            .first()
        )
        if i is None:
            abort(404)
        session.delete(i)
        session.commit()
        context = jsonify(
            {
                "status": "ok",
            }
        )
        return context
