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
from werkzeug.security import generate_password_hash, check_password_hash


class UserView(FlaskView):
    response = dict({"isLoggedIn": True})

    def index(self):
        pass

    @route("/login", methods=["POST"])
    def login(self):
        form = request.form
        for field in form:
            if form[field] == "" or form[field] is None:
                return jsonify(
                    {"isLoggedIn": False, "message": "All fields are required"}
                )

        uModel = MF.getModel("user")
        user = uModel.query.filter_by(email=form["email"]).first()
        if user:
            if check_password_hash(user.password, form["password"]):
                token = generate_password_hash(
                    form["password"] + user.fullname, method="sha256"
                )
                device = MF.getModel("device").newDevice(None, token, user.user_id)
                try:
                    db.session.add(device)
                    db.session.commit()
                    return jsonify(
                        {
                            "isLoggedIn": True,
                            "message": "Login successful",
                            "user": SF.getSchema("user", False).dump(user),
                            "token": token
                        }
                    )
                except Exception as e:
                    print(e)
                    return jsonify(
                        {"isLoggedIn": False, "message": "Incorrect credentials"}
                    )
            else:
                return jsonify(
                    {"isLoggedIn": False, "message": "Incorrect credentials"}
                )
        else:
            return jsonify({"isLoggedIn": False, "message": "Incorrect credentials"})


    @route("/signup/", methods=["POST"])
    def signup(self):
        print(request)
        form = request.form
        for field in form:
            if form[field] == "" or form[field] is None:
                return jsonify(
                    {"isRegistered": False, "message": "All fields are required"}
                )

        uModel = MF.getModel("user")
        checkUser = uModel.query.filter_by(email=form["email"]).count()
        if checkUser > 0:
            return jsonify(
                {"isRegistered": False, "message": "The email is already taken."}
            )

        hashed_password = generate_password_hash(form["password"], method="sha256")
        token = generate_password_hash(
            form["password"] + form["firstname"], method="sha256"
        )
        new_user = uModel.newUser(first_name=form['firstname'],
                                  last_name=form['lastname'],
                                  email=form['email'],
                                  password=hashed_password,
                                  login_type=1)
        try:
            db.session.add(new_user)
            db.session.commit()

            try:
                device = MF.getModel("device").newDevice(None, token, new_user.user_id)
                db.session.add(device)
                db.session.commit()
                return jsonify(
                    {
                        "isRegistered": True,
                        "message": "Regsiteration successful",
                        "user": SF.getSchema("user", False).dump(new_user),
                        "token": device.token
                    }
                )
            except Exception as e:
                return jsonify({"isRegistered": False, "message": "User Registered, "
                                                                  + "but login token was not generated."
                                                                    "Please Login manually"})
        except Exception as e:
            print(e)
            return jsonify({"isRegistered": False, "message": str(e)})


    @route("/my_profile/", methods=['GET', 'POST'])
    def my_profile(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)
        if request.method == "GET":
            return jsonify(SF.getSchema("user", False).dump(user))
        elif request.method == "POST":
            pass


    @route("/profile/<int:user_id>")
    def player_profile(self, user_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        isFound, user_pf = BL.getBL("user").getUserObjectById(user_id)
        if not isFound:
            return jsonify(invalidArgsResponse)

        user = BL.getBL("user").getUserProfileAsDump(user, user_pf)
        self.response.update({"user_profile": user})
        return jsonify(self.response)


    @route("/statuses/<int:player_id>/<int:offset>")
    def statuses(self, player_id, offset):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        app_offset = 0
        offset = int(offset)
        if offset > 0:
            app_offset = offset * request.args.get("offset")

        statuses = BL.getBL("status").getPlayerStatuses(user, player_id, app_offset)
        self.response.update({"statuses": statuses})
        return jsonify(self.response)

#
# @route("/club_followers/<int:club_id>")
# def clubFollowers(self, club_id):
#     user = AuthorizeRequest(request.headers)
#     if not user:
#         return jsonify(notLoggedIn)
#     club = self.cl.getClubObjById(club_id)
#     if not club:
#         return jsonify(invalidArgsResponse)
#
#     followers = self.fl.getClubFollowersForTab(user, club_id)
#     self.response.update({"followers": followers});
#     return jsonify(self.response)
#
#
# @route("/user/<int:user_id>", methods=['GET', 'POST'])
# def followUser(self, user_id):
#     user = AuthorizeRequest(request.headers)
#     if not user:
#         return jsonify(notLoggedIn)
#
#     isUserFound ,user_to_follow = self.ubl.getUserObjectById(user_id)
#     if not isUserFound:
#         return jsonify(invalidArgsResponse)
#
#     isFollowed, message, msg_type = self.fl.followUser(user, user_to_follow)
#     self.response.update({"isFollowed": isFollowed, "message": message, "msg_type": msg_type})
#     return jsonify(self.response)
