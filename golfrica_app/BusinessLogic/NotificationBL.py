from golfrica_app.Factories.ModelFactory import MF
from golfrica_app.Factories.SchemaFactory import SF
from datetime import datetime
from golfrica_app import db
from sqlalchemy import or_, text


class NotificationBL:

    @staticmethod
    def notifyUser(user, action, status):
        model = MF.getModel("notification")
        if action is "like":
            model.is_like = 1
        elif action is "share":
            model.is_share = 1
        elif action is "review":
            model.is_review = 1

        model.status_id = status.status_id
        model.to_be_notified_user_id = status.user_id
        model.notifier_user_id = user.user_id

        try:
            db.session.add(model)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    def getUserNotifications(self, user):
        sql = text(
            "SELECT notifications.*, users.user_id, users.first_name, users.last_name,users.profile_image FROM notifications "
            + " LEFT JOIN users on users.user_id = notifications.notifier_user_id "
            + " WHERE to_be_notified_user_id = " + str(user.user_id)
            + " ORDER BY notification_id DESC"
        )
        notifications = db.engine.execute(sql)
        return notifications.rowcount, SF.getSchema("notification").dump(notifications)

    def getNotficationsCount(self, user):
        action_notifications = 0
        swap_notification = 0
        action_notifications = MF.getModel("notification").query.filter_by(to_be_notified_user_id=user.user_id).count()
        swap_notification = MF.getModel("swap").query.filter_by(swaped_with_id=user.user_id).count()
        return action_notifications+swap_notification

