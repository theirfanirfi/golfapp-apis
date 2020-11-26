from flask import jsonify, request
from flask_classful import FlaskView, route

from golfrica_app.BusinessLogic.StatusesBL import StatusesBL
from golfrica_app.BusinessLogic.UsersBL import UsersBL
from golfrica_app.Globals.JSONResponses import AuthorizeRequest, notLoggedIn, dataSavedResponse, dataNotSavedResponse
class Statuses(FlaskView):
    response = dict({"isLoggedIn": True})
    bl = StatusesBL()
    ubl = UsersBL()
    def index(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        self.response.update({"statuses":self.bl.getSMStatuses()})
        return self.response

    def get(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        self.response.update({"country": self.bl.getCountryById(id)})
        return jsonify(self.response)

    @route("/like_status/<int:status_id>/")
    def likeStatus(self, status_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)
        isFound, status = self.bl.getStatusByIdObject(status_id)
        if isFound:
            isLiked, message, msg_type = self.bl.likeStatus(user, status)
            self.response.update({
                "isLiked": isLiked,
                "message": message,
                "msg_type": msg_type
            })
            return jsonify(self.response)
        self.response.update({
            "isLiked": False,
            "message": 'No such status found',
            "msg_type": 'error'
        })
        return jsonify(self.response)

    @route("/comment_status/", methods=['post'])
    def commentStatus(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)
        status_id = request.form['status_id']
        comment = request.form['comment']
        isFound, status = self.bl.getStatusByIdObject(status_id)
        if isFound:
            isCommented, message, msg_type = self.bl.commentStatus(user, status, comment)
            self.response.update({
                "isCommented": isCommented,
                "message": message,
                "msg_type": msg_type
            })
            return jsonify(self.response)
        self.response.update({
            "isCommented": False,
            "message": 'No such status found',
            "msg_type": 'error'
        })
        return jsonify(self.response)

    @route("/rate_status/<int:status_id>/<float:rating>")
    def rateStatus(self, status_id, rating):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)
        isFound, status = self.bl.getStatusByIdObject(status_id)
        if isFound:
            isRated, message, msg_type = self.bl.rateStatus(user, status, rating)
            self.response.update({
                "isRated": isRated,
                "message": message,
                "msg_type": msg_type
            })
            return jsonify(self.response)
        self.response.update({
            "isRated": False,
            "message": 'No such status found',
            "msg_type": 'error'
        })
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