from flask import jsonify, request, escape
from flask_classful import FlaskView, route

from golfrica_app.BusinessLogic.RatingBL import RatingBL
from golfrica_app.BusinessLogic.ClubsBL import ClubsBL
from golfrica_app.Globals.JSONResponses import AuthorizeRequest, notLoggedIn, dataSavedResponse,\
    dataNotSavedResponse, b64_to_data, invalidArgsResponse, get_decoded

class Rating(FlaskView):
    response = dict({"isLoggedIn": True})
    rl = RatingBL()
    cl = ClubsBL()
    def index(self):
        pass

    @route("rate_club/<int:club_id>", methods=['GET', 'POST'])
    def rate_club(self, club_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        club = self.cl.getClubObjById(club_id)
        if not club:
            return jsonify(invalidArgsResponse)

        if request.method == "GET":
            rating = self.rl.getClubAverageRating(club_id)
            self.response.update({"club_avg_rating": rating[0], 'total_reviews': rating[1]});
            return jsonify(self.response)
        elif request.method == "POST":
            data = get_decoded(request.form['data'])
            if not data or not ('review' in data or 'rating_stars' in data):
                self.response.update({
                    "isRated": False,
                    "message": 'Invalid data provided.',
                    "msg_type": 'error'
                })
                return jsonify(self.response)

            isClubRated, message, msg_type = self.rl.rateClub(user, club, data)
            self.response.update({"isRated": isClubRated, "message": message, "msg_type": msg_type})
            return jsonify(self.response)

        else:
            self.response.update({"isError": True, "message": "Invalid request", "msg_type": 'error'})
            return self.response

