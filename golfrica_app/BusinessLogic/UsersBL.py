from golfrica_app.Models.models import User, UserSchema
from datetime import datetime
from golfrica_app.Models.models import Country
from golfrica_app import db
from sqlalchemy import or_, text


class UsersBL:
    us = UserSchema(many=True)

    def getUsers(self):
        users = User.query.all()
        return self.us.dump(users)

    def getUserObjectById(self, id):
        user = User.query.filter_by(user_id=id)
        if user.count() > 0:
            return True, user.first()
        return False, False

    def getUserById(self, id):
        user = User.query.filter_by(user_id=id)
        if user.count() > 0:
            self.us.many = False
            return self.us.dump(user.first())
        return False

    def getUserProfileAsDump(self, user, user_pf):
        sql = text(
            "SELECT users.*, count(follows.f_id) as followers, IF(follows.follower_id = "
            + str(user.user_id)
            + ", true, false) as is_followed "
            + "FROM users LEFT JOIN follows on follows.followed_id = users.user_id AND is_user_followed = 1 "
            + "WHERE users.user_id = "
            + str(user_pf.user_id)
            + " GROUP BY follower_id"
        )
        user = db.engine.execute(sql)
        return self.us.dump(user)
