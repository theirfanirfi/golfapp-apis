from flask import jsonify, request, escape
from flask_classful import FlaskView, route

from golfrica_app.BusinessLogic.ClubsBL import ClubsBL
from golfrica_app.BusinessLogic.RatingBL import RatingBL
from golfrica_app.BusinessLogic.SyncStatuses import SyncStatuses
from golfrica_app.Models.models import Club
from golfrica_app.Globals.JSONResponses import AuthorizeRequest, notLoggedIn, dataSavedResponse,\
    dataNotSavedResponse, b64_to_data, invalidArgsResponse

class Clubs(FlaskView):
    response = dict({"isLoggedIn": True})
    cl = ClubsBL()
    rl = RatingBL()
    def index(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        self.response.update({"clubs":self.cl.getClubs()})
        return jsonify(self.response)

    def get(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        club = self.cl.getClubById(id)
        if not club:
            return jsonify(invalidArgsResponse)

        rating = self.rl.getClubAverageRating(id)
        self.response.update({
            "club": club,
            "club_avg_rating": rating[0],
            "total_reviews": rating[1],
            "isError": False,
            "club_descriptions": self.cl.getClubDescriptionWithUsers(id)
        })
        return jsonify(self.response)

    def country(self, country):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        self.response.update({"clubs": self.cl.getClubsByCountry(country)})
        return jsonify(self.response)

    def put(self):
        form = request.form
        #update profile description

    def post(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        form = request.form
        # numberOfInputs = len(form)
        # if numberOfInputs < 18:
        #     return 'all inputs must be provided'

        club = Club()
        for field in form:
            if not hasattr(Club, field):
                dataNotSavedResponse.update({"message": field + ' Invalid input.'})
                return jsonify(dataNotSavedResponse)
            elif form[field] == "":
                dataNotSavedResponse.update({"message": field + ' value must be provided'})
                return jsonify(dataNotSavedResponse)
            setattr(Club,field, escape(form[field]))


        isSaved, clubOrException = self.bl.addCountry(form)
        if isSaved:
            dataSavedResponse.update({"country": clubOrException})
            return jsonify(dataSavedResponse)
        dataNotSavedResponse.update({"message": clubOrException})
        return jsonify(dataNotSavedResponse)

    def delete(self, id):
        pass

    def sync_club_statuses(self):
        clubs = self.cl.getClubs()
        sync = SyncStatuses()
        for club in clubs:
            sync.sync_club_fb_status(club)

    @route("club_description/<int:club_id>", methods=['GET', 'POST'])
    def clubDescription(self, club_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        if request.method == "GET":
            club_descriptions = self.cl.getClubDescriptionWithUsers(club_id)
            # if not club_descriptions:
            #     return jsonify(invalidArgsResponse)
            self.response.update({"club_descriptions": club_descriptions});
            return jsonify(self.response)
        elif request.method == "POST":
            desc = b64_to_data(request.form['desc'])
            if not desc:
                return jsonify(invalidArgsResponse)

            isDescriptionUpdate, message, msg_type = self.cl.addClubDescriptoin(user, club_id, desc)
            self.response.update({"isUpdated": isDescriptionUpdate, "message": message, "msg_type": msg_type})
            return jsonify(self.response)

        else:
            return 'invalid request'

