from flask import jsonify, request, escape
from flask_classful import FlaskView, route
from golfrica_app.Models.models import User
from golfrica_app.BusinessLogic.PlayerBL import PlayerBL
from golfrica_app.BusinessLogic.ClubsBL import ClubsBL
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


class Player(FlaskView):
    response = dict({"isLoggedIn": True})
    pl = PlayerBL()
    cl = ClubsBL()

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

    @route("/profile/<int:player_id>")
    def player_profile(self, player_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        player = BL.getBL("player").getPlayerObjById(player_id)
        if not player:
            return jsonify(invalidArgsResponse)

        player = BL.getBL("player").getPlayeProfileAsDump(user, player)
        self.response.update({"player": player})
        return jsonify(self.response)

    @route("/statuses/<int:player_id>/<int:offset>")
    def statuses(self, player_id, offset):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        app_offset = 0
        offset = int(offset)
        if offset > 0:
            app_offset = offset * request.args.get("offset")

        statuses = BL.getBL("status").getPlayerStatuses(user, player_id, app_offset)
        self.response.update({"statuses": statuses})
        return jsonify(self.response)

    #
    # @route("/club_followers/<int:club_id>")
    # def clubFollowers(self, club_id):
    #     user = AuthorizeRequest(request.headers)
    #     if not user:
    #         return jsonify(notLoggedIn)
    #     club = self.cl.getClubObjById(club_id)
    #     if not club:
    #         return jsonify(invalidArgsResponse)
    #
    #     followers = self.fl.getClubFollowersForTab(user, club_id)
    #     self.response.update({"followers": followers});
    #     return jsonify(self.response)
    #
    #
    # @route("/user/<int:user_id>", methods=['GET', 'POST'])
    # def followUser(self, user_id):
    #     user = AuthorizeRequest(request.headers)
    #     if not user:
    #         return jsonify(notLoggedIn)
    #
    #     isUserFound ,user_to_follow = self.ubl.getUserObjectById(user_id)
    #     if not isUserFound:
    #         return jsonify(invalidArgsResponse)
    #
    #     isFollowed, message, msg_type = self.fl.followUser(user, user_to_follow)
    #     self.response.update({"isFollowed": isFollowed, "message": message, "msg_type": msg_type})
    #     return jsonify(self.response)
