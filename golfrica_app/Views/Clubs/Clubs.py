from flask import jsonify, request, escape
from flask_classful import FlaskView, route
from golfrica_app.BusinessLogic.SyncStatuses import SyncStatuses
from golfrica_app.Models.models import Club
from golfrica_app.Globals.JSONResponses import (
    AuthorizeRequest,
    notLoggedIn,
    dataSavedResponse,
    dataNotSavedResponse,
    b64_to_data,
    invalidArgsResponse,
)

from golfrica_app.Globals.ImageUpload import uploadMultipleImages
from golfrica_app.Factories.BLFactory import BL


class Clubs(FlaskView):
    response = dict({"isLoggedIn": True})

    def index(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        self.response.update({"clubs": BL.getBL("club").getClubs(user)})
        return jsonify(self.response)

    def get(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        club = BL.getBL("club").getClubProfile(id, user)
        if not club:
            return jsonify(invalidArgsResponse)

        rating = BL.getBL("rating").getClubAverageRating(id)
        self.response.update(
            {
                "club": club,
                "club_avg_rating": rating[0],
                "total_reviews": rating[1],
                "isError": False,
                "club_descriptions": BL.getBL("club").getClubDescriptionWithUsers(id),
            }
        )
        return jsonify(self.response)

    def country(self, country):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        self.response.update({"clubs": BL.getBL("club").getClubsByCountry(country)})
        return jsonify(self.response)

    def put(self):
        form = request.form
        # update profile description

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
                dataNotSavedResponse.update({"message": field + " Invalid input."})
                return jsonify(dataNotSavedResponse)
            elif form[field] == "":
                dataNotSavedResponse.update(
                    {"message": field + " value must be provided"}
                )
                return jsonify(dataNotSavedResponse)
            setattr(Club, field, escape(form[field]))

        isSaved, clubOrException = self.bl.addCountry(form)
        if isSaved:
            dataSavedResponse.update({"country": clubOrException})
            return jsonify(dataSavedResponse)
        dataNotSavedResponse.update({"message": clubOrException})
        return jsonify(dataNotSavedResponse)

    def delete(self, id):
        pass

    def sync_club_statuses(self):
        clubs = BL.getBL("club").getClubs()
        sync = SyncStatuses()
        for club in clubs:
            sync.sync_club_fb_status(club)

    @route("club_description/<int:club_id>", methods=["GET", "POST"])
    def clubDescription(self, club_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        if request.method == "GET":
            club_descriptions = BL.getBL("club").getClubDescriptionWithUsers(club_id)
            # if not club_descriptions:
            #     return jsonify(invalidArgsResponse)
            self.response.update({"club_descriptions": club_descriptions})
            return jsonify(self.response)
        elif request.method == "POST":
            desc = b64_to_data(request.form["desc"])
            if not desc:
                return jsonify(invalidArgsResponse)

            media = uploadMultipleImages(request.files, "clubs/description", user)
            isDescriptionUpdate, message, msg_type = BL.getBL(
                "club"
            ).addClubDescriptoin(user, club_id, desc, media)
            self.response.update(
                {
                    "isUpdated": isDescriptionUpdate,
                    "message": message,
                    "msg_type": msg_type,
                }
            )
            return jsonify(self.response)

        else:
            return "invalid request"

    @route("/statuses/<int:club_id>/<int:offset>")
    def statuses(self, club_id, offset):
        print("working")
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        app_offset = 0
        offset = int(offset)
        if offset > 0:
            app_offset = offset * request.args.get("offset")

        statuses = BL.getBL("status").getClubStatuses(user, club_id, app_offset)
        self.response.update({"statuses": statuses})
        return jsonify(self.response)
