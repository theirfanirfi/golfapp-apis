from golfrica_app.Factories.SchemaFactory import SF
from golfrica_app.Factories.ModelFactory import MF
from datetime import datetime
from golfrica_app import db
from sqlalchemy import or_, text


class ParticipantBL:
    def getUserChats(self, user):
        sql = text(
            "SELECT *, IF(chat_participants.`chat_initiater_id` = "
            + str(user.user_id)
            + ", true, false) as i_am_intitiater, "
            + "(select messages.message from message WHERE messages.p_id = chat_participants.p_id ORDER BY msg_id DESC LIMIT 1) as last_message, "
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
        pass
