from flask import jsonify, request
from flask_classful import FlaskView, route

from golfrica_app.BusinessLogic.CommentBL import CommentBL
from golfrica_app.BusinessLogic.UsersBL import UsersBL
from golfrica_app.BusinessLogic.SwapBL import SwapBL
from golfrica_app.BusinessLogic.StatusesBL import StatusesBL
from golfrica_app.Globals.JSONResponses import AuthorizeRequest, notLoggedIn, dataSavedResponse,\
    dataNotSavedResponse, get_decoded
class Swap(FlaskView):
    response = dict({"isLoggedIn": True})
    bl = SwapBL()
    ubl = UsersBL()
    sbl = StatusesBL()
    def index(self):
        pass


    def get(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        self.response.update({"country": self.bl.getCountryById(id)})
        return jsonify(self.response)

    @route("/status/<int:status_id>/")
    def swap_status(self, status_id):
        print(request.headers)
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)
        isFound, status = self.sbl.getStatusByIdObject(status_id)
        if not isFound:
            self.response.update({
                "isSwaped": False,
                'message': 'Status not found.',
                'msg_type': 'error'
            })

        isSwaped, message, msg_type = self.bl.swapStatus(user, status)
        self.response.update({
            "isSwaped": isSwaped,
            'message': message,
            'msg_type': msg_type
        })
        return jsonify(self.response)

    @route("/comment_status/", methods=['post'])
    def commentStatus(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)
        print(request.form['data'])
        data = get_decoded(request.form['data'])
        print(data)
        if not data:
            self.response.update({
                "isCommented": False,
                "messageOrComment": 'Invalid data provided.',
                "msg_type": 'error'
            })
            return jsonify(self.response)

        statusObj = StatusesBL()
        isFound, status = statusObj.getStatusByIdObject(data['status_id'])
        if isFound:
            isCommented, messageOrComment, msg_type = self.bl.commentStatus(user, status, data['comment'], data['rating'])
            self.response.update({
                "isCommented": isCommented,
                "messageOrComment": messageOrComment,
                "msg_type": msg_type
            })
            return jsonify(self.response)
        self.response.update({
            "isCommented": False,
            "messageOrComment": 'No such status found',
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