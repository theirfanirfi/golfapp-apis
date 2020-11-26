from flask_classful import FlaskView
from flask import jsonify, request
from golfrica_app.Models.models import Country
from golfrica_app import app

class GolfricaAuthJSONResponse(FlaskView):

    notLoggedIndata = dict({
        "isLoggedIn": False,
        'message': 'Your are not logged in'
    })
    isLoggedIn = True
    headers = []

    def return_json(self,data):
        if not self.isLoggedIn:
            return jsonify(self.notLoggedIndata)
        data.update({"isLoggedIn": True})
        return jsonify(data)

    def AuthorizeRequest(self):
        if not 'Authorization' in self.headers:
            self.isLoggedIn = False
        else:
            self.isLoggedIn = True

