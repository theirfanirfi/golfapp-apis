from flask import jsonify, request, escape
from flask_classful import FlaskView, route
from golfrica_app.Models.models import User
from golfrica_app.BusinessLogic.FollowBL import FollowBL
from golfrica_app.BusinessLogic.ClubsBL import ClubsBL
from golfrica_app.BusinessLogic.UsersBL import UsersBL
from golfrica_app.BusinessLogic.PlayerBL import PlayerBL
from golfrica_app.Globals.JSONResponses import AuthorizeRequest, notLoggedIn, dataSavedResponse,\
    dataNotSavedResponse, b64_to_data, invalidArgsResponse, get_decoded

class Follow(FlaskView):
    response = dict({"isLoggedIn": True})
    fl = FollowBL()
    cl = ClubsBL()
    ubl = UsersBL()
    pbl = PlayerBL()
    def index(self):
        pass

    @route("/club/<int:club_id>", methods=['GET', 'POST'])
    def followClub(self, club_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        club = self.cl.getClubObjById(club_id)
        if not club:
            return jsonify(invalidArgsResponse)

        if request.method == "GET":
            followers = self.fl.getClubFollowers(club_id)
            self.response.update({"followers": followers});
            return jsonify(self.response)
        elif request.method == "POST":
            isFollowed, message, msg_type = self.fl.followClub(user, club)
            self.response.update({"isFollowed": isFollowed, "message": message, "msg_type": msg_type})
            return jsonify(self.response)

        else:
            self.response.update({"isError": True, "message": "Invalid request", "msg_type": 'error'})
            return self.response

    @route("/club_followers/<int:club_id>")
    def clubFollowers(self, club_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)
        club = self.cl.getClubObjById(club_id)
        if not club:
            return jsonify(invalidArgsResponse)

        followers = self.fl.getClubFollowersForTab(user, club_id)
        self.response.update({"followers": followers});
        return jsonify(self.response)


    @route("/user/<int:user_id>", methods=['GET', 'POST'])
    def followUser(self, user_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        isUserFound ,user_to_follow = self.ubl.getUserObjectById(user_id)
        if not isUserFound:
            return jsonify(invalidArgsResponse)

        isFollowed, message, msg_type = self.fl.followUser(user, user_to_follow)
        self.response.update({"isFollowed": isFollowed, "message": message, "msg_type": msg_type})
        return jsonify(self.response)


    @route("/player/<int:player_id>", methods=['GET', 'POST'])
    def followUser(self, player_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        player_to_follow = self.pbl.getPlayerObjById(player_id)
        if not player_to_follow:
            return jsonify(invalidArgsResponse)

        isFollowed, message, msg_type = self.fl.followPlayer(user, player_to_follow)
        self.response.update({"isFollowed": isFollowed, "message": message, "msg_type": msg_type})
        return jsonify(self.response)
