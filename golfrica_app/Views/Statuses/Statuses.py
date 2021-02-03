from flask import jsonify, request
from flask_classful import FlaskView, route
from golfrica_app.Models.models import AlchemyEncoder
from golfrica_app.BusinessLogic.StatusesBL import StatusesBL
from golfrica_app.BusinessLogic.UsersBL import UsersBL
from golfrica_app.BusinessLogic.CommentBL import CommentBL
from golfrica_app.Globals.JSONResponses import (
    AuthorizeRequest,
    notLoggedIn,
    dataSavedResponse,
    dataNotSavedResponse,
)
from datetime import datetime
import json
import os
from werkzeug.utils import secure_filename
from golfrica_app import app


class Statuses(FlaskView):
    response = dict({"isLoggedIn": True})
    bl = StatusesBL()
    ubl = UsersBL()
    cbl = CommentBL()

    def index(self):
        offset = 0
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        if "offset" in request.args:
            offset = int(request.args.get("offset")) * 10
            print(offset)

        statuses = self.bl.getStatusesForFeed(user, offset)
        self.response.update({"statuses": statuses})
        return self.response

    def get(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        status = self.bl.getStatusByIdAsJsonDump(id)
        if not status:
            self.response.update(
                {
                    "isFound": False,
                    "message": "No such status found",
                    "msg_type": "error",
                }
            )

        status_comments = self.cbl.getStatusComments(id)
        self.response.update(
            {
                "isFound": False,
                "status": status,
                "comments": status_comments,
                "message": "loading",
                "msg_type": "info",
            }
        )
        return jsonify(self.response)

    @route("/like_status/<int:status_id>/")
    def likeStatus(self, status_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)
        isFound, status = self.bl.getStatusByIdObject(status_id)
        if isFound:
            isLiked, message, msg_type = self.bl.likeStatus(user, status)
            self.response.update(
                {"isLiked": isLiked, "message": message, "msg_type": msg_type}
            )
            return jsonify(self.response)
        self.response.update(
            {"isLiked": False, "message": "No such status found", "msg_type": "error"}
        )
        return jsonify(self.response)

    @route("/comment_status/", methods=["post"])
    def commentStatus(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)
        status_id = request.form["status_id"]
        comment = request.form["comment"]
        isFound, status = self.bl.getStatusByIdObject(status_id)
        if isFound:
            isCommented, message, msg_type = self.bl.commentStatus(
                user, status, comment
            )
            self.response.update(
                {"isCommented": isCommented, "message": message, "msg_type": msg_type}
            )
            return jsonify(self.response)
        self.response.update(
            {
                "isCommented": False,
                "message": "No such status found",
                "msg_type": "error",
            }
        )
        return jsonify(self.response)

    @route("/rate_status/<int:status_id>/<float:rating>")
    def rateStatus(self, status_id, rating):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)
        isFound, status = self.bl.getStatusByIdObject(status_id)
        if isFound:
            isRated, message, msg_type = self.bl.rateStatus(user, status, rating)
            self.response.update(
                {"isRated": isRated, "message": message, "msg_type": msg_type}
            )
            return jsonify(self.response)
        self.response.update(
            {"isRated": False, "message": "No such status found", "msg_type": "error"}
        )
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

    @route("/upload", methods=["GET", "POST"])
    def upload_media(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        if request.method == "GET":
            pass
        elif request.method == "POST":
            if request.form["status"] == "" and not request.files:
                self.response.update(
                    {"isStatusPosted": False, "status": "Enter text or upload images."}
                )
                return jsonify(self.response)

            data = {
                "status": None,
                "media": {"images": [], "video": []},
            }
            media = list()
            status_text = request.form["status"]
            data["status"] = status_text
            if request.files:
                files = request.files
                images = files.getlist("images[]")
                for image in images:
                    dt_obj = datetime.strptime(
                        str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f"
                    )
                    millisec = str(dt_obj.timestamp() * 1000)
                    time = millisec.replace(".", "")
                    image_name = user.first_name + str(user.user_id) + time + ".jpg"
                    media.append(image_name)

                    folder = os.path.join(app.root_path, 'static/user/status')
                    file_path = os.path.join(folder, image_name)

                    image.save(file_path)
                data["media"] = {"images": media, "video": []}
            isStatusPosted, status = self.bl.addUserStatus(user, data)
            self.response.update({"isStatusPosted": isStatusPosted, "status": status})
            return jsonify(self.response)
        else:
            return "invalid request"

    def delete(self, id):
        pass
