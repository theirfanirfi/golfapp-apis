from flask import jsonify, request
from flask_classful import FlaskView, route
from golfrica_app import db, app

from golfrica_app.Factories.BLFactory import BL
from golfrica_app.Factories.SchemaFactory import SF
from golfrica_app.Factories.ModelFactory import MF
from golfrica_app.Globals.JSONResponses import (
    AuthorizeRequest,
    notLoggedIn,
    invalidArgsResponse,
)


class NotificationView(FlaskView):
    response = dict({"isLoggedIn": True})

    def index(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        n_count, notifications = BL.getBL("notification").getUserNotifications(user)
        self.response.update({"notifications": notifications, "isFound": True if n_count > 0 else False})
        return jsonify(self.response)

    @route('/notification_count/')
    def notification_count(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        self.response.update(
            {"notifications_count": BL.getBL("notification").getNotficationsCount(user)}
        )

        return jsonify(self.response)
