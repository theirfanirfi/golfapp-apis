from flask import jsonify, request, escape
from flask_classful import FlaskView, route
from golfrica_app.Factories.BLFactory import  BL
from golfrica_app.Globals.JSONResponses import (
    AuthorizeRequest,
    notLoggedIn,
    dataSavedResponse,
    dataNotSavedResponse,
    b64_to_data,
    invalidArgsResponse,
    get_decoded,
)


class Follow(FlaskView):
    response = dict({"isLoggedIn": True})

    def index(self):
        pass

    @route("/club/<int:club_id>", methods=["GET", "POST"])
    def followClub(self, club_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        club = BL.getBL("club").getClubObjById(club_id)
        if not club:
            return jsonify(invalidArgsResponse)

        if request.method == "GET":
            followers = BL.getBL("follow").getClubFollowers(club_id)
            self.response.update({"followers": followers})
            return jsonify(self.response)
        elif request.method == "POST":
            isFollowed, message, msg_type = BL.getBL("follow").followClub(user, club)
            self.response.update(
                {"isFollowed": isFollowed, "message": message, "msg_type": msg_type}
            )
            return jsonify(self.response)

        else:
            self.response.update(
                {"isError": True, "message": "Invalid request", "msg_type": "error"}
            )
            return self.response

    @route("/player_followers/<int:player_id>")
    def playerFollowers(self, player_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)
        player = BL.getBL("player").getPlayerObjById(player_id)
        if not player:
            return jsonify(invalidArgsResponse)

        followers = BL.getBL("follow").getPlayerFollowersForTab(user, player_id)
        self.response.update({"followers": followers})
        return jsonify(self.response)

    @route("/club_followers/<int:club_id>")
    def clubFollowers(self, club_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)
        club = BL.getBL("club").getClubObjById(club_id)
        if not club:
            return jsonify(invalidArgsResponse)

        followers = BL.getBL("follow").getClubFollowersForTab(user, club_id)
        self.response.update({"followers": followers})
        return jsonify(self.response)

    @route("/user/<int:user_id>", methods=["GET", "POST"])
    def followUser(self, user_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        isUserFound, user_to_follow = BL.getBL("user").getUserObjectById(user_id)
        if not isUserFound:
            return jsonify(invalidArgsResponse)

        isFollowed, message, msg_type = BL.getBL("follow").followUser(user, user_to_follow)
        self.response.update(
            {"isFollowed": isFollowed, "message": message, "msg_type": msg_type}
        )
        return jsonify(self.response)

    @route("/player/<int:player_id>", methods=["GET", "POST"])
    def followPlayer(self, player_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        player_to_follow = BL.getBL("player").getPlayerObjById(player_id)
        if not player_to_follow:
            return jsonify(invalidArgsResponse)

        isFollowed, message, msg_type = BL.getBL("follow").followPlayer(user, player_to_follow)
        self.response.update(
            {"isFollowed": isFollowed, "message": message, "msg_type": msg_type}
        )
        return jsonify(self.response)

    @route('/get_followed/')
    def getFollowed(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        followed = BL.getBL("follow").getFollowedUsers(user)
        return jsonify(followed)
