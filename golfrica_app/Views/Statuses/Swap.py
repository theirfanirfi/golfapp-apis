from flask import jsonify, request
from flask_classful import FlaskView, route
from golfrica_app.Factories.BLFactory import BL
from golfrica_app.Globals.JSONResponses import AuthorizeRequest, notLoggedIn, dataSavedResponse,\
    dataNotSavedResponse, get_decoded
class Swap(FlaskView):
    response = dict({"isLoggedIn": True})

    def index(self):
        print(request.headers)
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        swaps = BL.getBL("swap").getSwaps(user)
        return jsonify(swaps)

    def get(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        self.response.update({"country": BL.getBL("swap").getCountryById(id)})
        return jsonify(self.response)

    @route("/status/<int:status_id>/")
    def swap_status(self, status_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)
        isFound, status = BL.getBL("status").getStatusByIdObject(status_id)
        print(status.status_id)

        if not isFound:
            self.response.update({
                "isSwaped": False,
                'message': 'Status not found.',
                'msg_type': 'error'
            })

        isSwaped, message, msg_type = BL.getBL("swap").swapStatus(user, status)
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

        isFound, status = BL.getBL("status").getStatusByIdObject(data['status_id'])
        if isFound:
            isCommented, messageOrComment, msg_type = BL.getBL("swap").commentStatus(user, status, data['comment'], data['rating'])
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
        isUpdated, countryOrException = BL.getBL("swap").addCountry(form)
        if isUpdated:
            dataSavedResponse.update({"country": countryOrException})
            return jsonify(dataSavedResponse)
        dataNotSavedResponse.update({"message": countryOrException})
        return jsonify(dataNotSavedResponse)

    def delete(self, id):
        pass

    def notifications(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        isSwapNotificationsFound, swaps = BL.getBL("swap").getSwapNotifications(user)
        self.response.update({"isSwapNotificationsFound": isSwapNotificationsFound, "swaps": swaps})
        return jsonify(self.response)

    def approve(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        swap = BL.getBL("swap").getSwapObjectById(id)
        if not swap:
            self.response.update({"isSwapApproved": False, "message": 'Swap not found.','msg_type': 'error'})
            return jsonify(self.response)

        isSwapApproved, message, msg_type = BL.getBL("swap").approveSwap(user, swap)
        self.response.update({"isSwapApproved": isSwapApproved, "message": message, 'msg_type': msg_type})
        return jsonify(self.response)

    def decline(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        swap = BL.getBL("swap").getSwapObjectById(id)
        if not swap:
            self.response.update({"isSwapDeclined": False, "message": 'Swap not found.','msg_type': 'error'})
            return jsonify(self.response)

        isSwapDeclined, message, msg_type = BL.getBL("swap").declineSwap(user, swap)
        self.response.update({"isSwapDeclined": isSwapDeclined, "message": message, 'msg_type': msg_type})
        return jsonify(self.response)
