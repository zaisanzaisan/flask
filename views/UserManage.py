from flask import jsonify, request
from flask.views import MethodView

from models import User, get_session
from validators import UserValidate


class UsersManage(MethodView):
    def get(self):
        # request.json
        session = get_session()
        users = session.query(User).all()
        # session.close()
        context = dict()
        for cnt, user in enumerate(users):
            context[cnt] = {"uid": user.id, "name": user.name}
        context = jsonify(context)
        return context

    def post(self):
        validated_data = UserValidate(**request.json).dict()
        headers = request.headers
        qs = request.args
        session = get_session()
        usr = User(name=validated_data["name"])
        session.add(usr)
        session.commit()
        # session.close()
        context = jsonify({"status": "ok", "uid": usr.id, "name": usr.name})
        return context

    def patch(self):
        pass

    def delete(self):
        pass
