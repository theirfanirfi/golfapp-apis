from flask import jsonify, request
from flask_classful import FlaskView, route

from golfrica_app.BusinessLogic.LikeBL import LikeBL
from golfrica_app.BusinessLogic.UsersBL import UsersBL
from golfrica_app.BusinessLogic.StatusesBL import StatusesBL
from golfrica_app.Globals.JSONResponses import AuthorizeRequest, notLoggedIn, dataSavedResponse, dataNotSavedResponse
class Like(FlaskView):
    response = dict({"isLoggedIn": True})
    bl = LikeBL()
    ubl = UsersBL()
    sbl = StatusesBL()

    @route("/status/<int:status_id>/")
    def status(self, status_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        isFound, status = self.sbl.getStatusByIdObject(status_id)
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

    @route("/unlike/<int:status_id>/")
    def unlike(self, status_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)
        isFound, status = self.bl.getStatusByIdObject(status_id)
        if isFound:
            isUnLiked, message, msg_type = self.bl.unLikeStatus(user, status)
            self.response.update({
                "isUnLiked": isUnLiked,
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