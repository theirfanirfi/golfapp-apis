from golfrica_app.Models.models import Club, ClubSchema
from datetime import datetime
from golfrica_app.Models.models import Country
from golfrica_app import db
from sqlalchemy import or_

class ClubsBL:
    cs = ClubSchema(many=True)

    def getClubs(self):
        clubs= Club.query.all()
        return self.cs.dump(clubs)

    def getClubsForSync(self):
        clubs= Club.query.all()
        return clubs

    def getClubById(self, id):
        club = Club.query.filter_by(club_id=id)
        if club.count() > 0:
            self.cs.many = False
            return self.cs.dump(club.first())
        return False

    def getClubByName(self, name):
        club = Club.query.filter_by(club_name=name)
        if club.count() > 0:
            self.cs.many = False
            return self.cs.dump(club.first())
        return False

    def getClubsByCountry(self, country):
        clubs = Club.query.filter_by(club_country=country)
        if clubs.count() > 0:
            return self.cs.dump(clubs.all())
        return False


    def addClub(self, club):
        c = Club.query.filter_by(club_name=club.club_name)
        if c.count() > 0:
            return False, 'Club with the same name already exists'

        try:
            db.session.add(club)
            db.session.commit()
            self.cs.many=False
            return True, self.cs.dump(club)
        except Exception as ex:
            return False, str(ex)




