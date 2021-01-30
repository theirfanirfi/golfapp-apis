from golfrica_app.Factories.SchemaFactory import SF
from golfrica_app.Factories.ModelFactory import MF
from datetime import datetime
from golfrica_app import db
from sqlalchemy import or_, text


class ParticipantBL:
    def getUserChats(self, user):
        sql = text(
            "SELECT chat_participants.*, CONCAT(initiater.first_name,' ', initiater.last_name) as initiater_username,"
            + "CONCAT(initiated_with.first_name,' ', initiated_with.last_name) as initiated_with_username,"
            + "initiater.profile_image as initiater_profile_image, initiated_with.profile_image as initiated_with_profile_image,"
            + " IF(chat_participants.`chat_initiater_id` = "
            + str(user.user_id)
            + ", true, false) as i_am_intitiater, "
            + "(select messages.message from messages WHERE messages.p_id = chat_participants.p_id ORDER BY msg_id DESC LIMIT 1) as last_message, "
            + "(select count(*) from messages WHERE messages.p_id = chat_participants.p_id AND messages.is_read = 0) as unread_msgs "
            + "FROM chat_participants LEFT JOIN users as initiater on initiater.user_id = chat_participants.chat_initiater_id "
            + "LEFT JOIN users as initiated_with on initiated_with.user_id = chat_participants.chat_initiated_with_id "
            + "WHERE chat_initiater_id = "
            + str(user.user_id)
            + " or chat_initiated_with_id = "
            + str(user.user_id)
            + " ORDER BY unread_msgs DESC"
        )
        participants = db.engine.execute(sql)
        return SF.getSchema("participant").dump(participants)

    def getChatMessages(self, user, participant):
        sql = text(
            "SELECT messages.msg_id as _id, messages.message as text, messages.created_at as createdAt, "
            + "JSON_OBJECT('_id', users.user_id, 'name', users.first_name, 'avatar', users.profile_image ) as user FROM messages "
            + "LEFT JOIN users on users.user_id = messages.sender_id WHERE messages.p_id = "
            + str(participant.p_id)
            + " ORDER BY msg_id DESC"
        )
        return SF.getSchema("chat").dump(db.engine.execute(sql))

    def getChatMessagesForUser(self, user, user_pf):
        sql = text(
            "SELECT messages.msg_id as _id, messages.message as text, messages.created_at as createdAt, "
            + "JSON_OBJECT('_id', users.user_id, 'name', users.first_name, 'avatar', users.profile_image ) as user FROM messages "
            + "LEFT JOIN users on users.user_id = messages.sender_id WHERE (messages.sender_id = "
            + str(user.user_id)
            + " AND messages.receiver_id = "
            + str(user_pf.user_id)
            + ") or (messages.receiver_id = "
            + str(user.user_id)
            + " AND messages.sender_id = "
            + str(user_pf.user_id)
            + ")"
            + " ORDER BY msg_id DESC"
        )
        return SF.getSchema("chat").dump(db.engine.execute(sql))

    def getParticipantObject(self, id):
        participant = MF.getModel("participant").query.filter_by(p_id=id)
        return participant.first() if participant.count() > 0 else False

    def checkParticipant(self, user, receiver_id):
        sql = text(
            "SELECT * FROM chat_participants WHERE (chat_initiater_id = "
            + str(user.user_id)
            + " AND chat_initiated_with_id ="
            + str(receiver_id)
            + ") "
            + "OR (chat_initiater_id = "
            + str(receiver_id)
            + " AND chat_initiated_with_id ="
            + str(user.user_id)
            + ")"
        )
        participant = db.engine.execute(sql)
        return participant.rowcount, participant.first()

    def createParticipants(self, user, receiver_id):
        try:
            new_participant = MF.getModel("participant")
            new_participant.chat_initiater_id = user.user_id
            new_participant.chat_initiated_with_id = receiver_id
            db.session.add(new_participant)
            db.session.commit()
            return True, new_participant
        except Exception as e:
            print(e)
            return False, str(e)
