from flask import jsonify, request
from flask_classful import FlaskView

from golfrica_app.BusinessLogic.SyncStatuses import SyncStatuses
from golfrica_app.Globals.JSONResponses import AuthorizeRequest, notLoggedIn, dataSavedResponse, dataNotSavedResponse

class Sync(FlaskView):
    response = dict({"isLoggedIn": True})
    bl = SyncStatuses()
    def index(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        self.response.update({"statuses":self.bl.getSMStatuses()})
        return jsonify(self.response)

    def fb(self):
        self.bl.sync_club_fb_status()
        return str(self.bl.sync_club_fb_status())


    def get(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        self.response.update({"country": self.bl.getCountryById(id)})
        return jsonify(self.response)


    def put(self):
        pass

    def post(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        form = request.form
        isUpdated, countryOrException = self.bl.addCountry(form)
        if isUpdated:
            dataSavedResponse.update({"country": countryOrException})
            return jsonify(dataSavedResponse)
        dataNotSavedResponse.update({"message": countryOrException})
        return jsonify(dataNotSavedResponse)

    def delete(self, id):
        pass