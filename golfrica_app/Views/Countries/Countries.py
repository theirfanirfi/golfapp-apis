from flask import jsonify, request
from flask_classful import FlaskView

from golfrica_app.BusinessLogic.CountriesBL import CountryBL
from golfrica_app.Globals.JSONResponses import AuthorizeRequest, notLoggedIn, dataSavedResponse, dataNotSavedResponse

class Countries(FlaskView):
    response = dict({"isLoggedIn": True})
    bl = CountryBL()
    def index(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        self.response.update({"countries":self.bl.getCountries()})
        return jsonify(self.response)

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