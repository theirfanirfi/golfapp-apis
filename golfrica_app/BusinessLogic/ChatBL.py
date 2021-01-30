from golfrica_app.Factories.ModelFactory import MF
from golfrica_app.Factories.SchemaFactory import SF
from datetime import datetime
from golfrica_app import db
from sqlalchemy import or_, text


class ChatBL:
    def sendMessage(self, user, receiver, text, participant):
        schema = SF.getSchema("participant")
        schema.many = False
        new_msg = MF.getModel("messages")
        new_msg.sender_id = user.user_id
        new_msg.receiver_id = receiver.user_id
        new_msg.message = text
        new_msg.p_id = participant.p_id

        try:
            db.session.add(new_msg)
            db.session.commit()
            return True, schema.dump(new_msg)
        except Exception as e:
            print(e)
            return False, str(e)
