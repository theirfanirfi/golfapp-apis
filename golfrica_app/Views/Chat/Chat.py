from flask import jsonify, request, escape
from flask_classful import FlaskView, route
from golfrica_app.Models.models import User
from golfrica_app.Factories.BLFactory import BL
from golfrica_app.Globals.JSONResponses import (
    AuthorizeRequest,
    notLoggedIn,
    dataSavedResponse,
    dataNotSavedResponse,
    b64_to_data,
    invalidArgsResponse,
    get_decoded,
)


class Chat(FlaskView):
    response = dict({"isLoggedIn": True})

    def index(self):
        pass

    def get(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        club = self.cl.getClubObjById(id)
        if not club:
            return jsonify(invalidArgsResponse)

        self.response.update({"players": BL.getBL("player").getPlayers(user, club)})
        return jsonify(self.response)
