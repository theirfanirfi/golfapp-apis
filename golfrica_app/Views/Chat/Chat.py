from flask import jsonify, request, escape
from flask_classful import FlaskView, route
from golfrica_app.Models.models import User
from golfrica_app.Factories.BLFactory import BL
from golfrica_app.Factories.SchemaFactory import SF
from golfrica_app.Globals.JSONResponses import (
    AuthorizeRequest,
    notLoggedIn,
    dataSavedResponse,
    dataNotSavedResponse,
    b64_to_data,
    invalidArgsResponse,
    get_decoded,
)


class Chat(FlaskView):
    response = dict({"isLoggedIn": True})

    def index(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        participants = BL.getBL("participant").getUserChats(user)
        self.response.update({"participants": participants})
        return jsonify(self.response)

    def get(self, id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        participant = BL.getBL("participant").getParticipantObject(id)
        if not participant:
            return jsonify(invalidArgsResponse)

        messages = BL.getBL("participant").getChatMessages(user, participant)
        pschema = SF.getSchema("participant")
        pschema.many = False
        participant = pschema.dump(participant)
        self.response.update({"messages": messages, "participants": participant})
        return jsonify(self.response)

    @route("/get_chat_messages/<int:user_two_id>/")
    def get_chat_messages(self, user_two_id):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        isUserTwo, user_two = BL.getBL("user").getUserObjectById(user_two_id)
        if not isUserTwo:
            return jsonify(invalidArgsResponse)

        pCount, participant = BL.getBL("participant").checkParticipant(
            user, user_two.user_id
        )

        messages = BL.getBL("participant").getChatMessagesForUser(user, user_two)
        pschema = SF.getSchema("participant")
        pschema.many = False
        participant = pschema.dump(participant)
        self.response.update({"messages": messages, "participants": participant})
        return jsonify(self.response)

    def post(self):
        user = AuthorizeRequest(request.headers)
        if not user:
            return jsonify(notLoggedIn)

        form = request.form
        for f in form:
            if form[f] == None or form[f] == "":
                return jsonify(invalidArgsResponse)

        text = b64_to_data(form["text"])
        receiver_id = form["receiver_id"]
        p_id = form["p_id"]
        participant = None

        isFound, receiver = BL.getBL("user").getUserObjectById(receiver_id)
        if not isFound:
            return jsonify(invalidArgsResponse)

        isParticipantFound, participant = BL.getBL("participant").checkParticipant(
            user, receiver_id
        )
        if not isParticipantFound > 0:
            isParticipantsCreated, participant = BL.getBL(
                "participant"
            ).createParticipants(user, receiver_id)
            if not isParticipantsCreated:
                return jsonify(invalidArgsResponse)

        isMessageSent, msg = BL.getBL("chat").sendMessage(
            user, receiver, text, participant
        )

        if not isMessageSent:
            print("message not sent")
            return jsonify(invalidArgsResponse)

        self.response.update({"isMessageSent": True, "message": msg})
        return jsonify(self.response)