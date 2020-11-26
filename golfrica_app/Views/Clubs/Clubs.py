from flask import jsonify, request, escape
from flask_classful import FlaskView, route

from golfrica_app.BusinessLogic.ClubsBL import ClubsBL
from golfrica_app.BusinessLogic.SyncStatuses import SyncStatuses
from golfrica_app.Models.models import Club
from golfrica_app.Globals.JSONResponses import AuthorizeRequest, notLoggedIn, dataSavedResponse, dataNotSavedResponse

class Clubs(FlaskView):
    response = dict({"isLoggedIn": True})
    cl = ClubsBL()
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

        self.response.update({"club": self.cl.getClubById(id)})
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

