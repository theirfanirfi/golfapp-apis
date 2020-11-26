from golfrica_app.Models.models import User, UserSchema
from datetime import datetime
from golfrica_app.Models.models import Country
from golfrica_app import db
from sqlalchemy import or_

class UsersBL:
    us = UserSchema(many=True)

    def getClubs(self):
        clubs= User.query.all()
        return self.us.dump(clubs)

    def getClubsForSync(self):
        clubs= User.query.all()
        return clubs

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

    def getClubByName(self, name):
        club = User.query.filter_by(club_name=name)
        if club.count() > 0:
            self.us.many = False
            return self.us.dump(club.first())
        return False

    def getClubsByCountry(self, country):
        clubs = User.query.filter_by(club_country=country)
        if clubs.count() > 0:
            return self.us.dump(clubs.all())
        return False


    def addClub(self, club):
        c = User.query.filter_by(club_name=club.club_name)
        if c.count() > 0:
            return False, 'Club with the same name already exists'

        try:
            db.session.add(club)
            db.session.commit()
            self.us.many=False
            return True, self.us.dump(club)
        except Exception as ex:
            return False, str(ex)




