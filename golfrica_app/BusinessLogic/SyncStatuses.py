from golfrica_app.Models.models import Status, StatusSchema
from datetime import datetime
from golfrica_app.Models.models import Club
from golfrica_app.BusinessLogic.StatusesBL import StatusesBL
from golfrica_app.BusinessLogic.ClubsBL import ClubsBL
from golfrica_app import db
from sqlalchemy import or_
from facebook_scraper import get_posts

class SyncStatuses:
    ss = StatusSchema(many=True)

    def getClubs(self):
        clubs= Status.query.all()
        return self.ss.dump(clubs)

    def getClubById(self, id):
        club = Status.query.filter_by(club_id=id)
        if club.count() > 0:
            self.cs.many = False
            return self.ss.dump(club.first())
        return False

    def getClubByName(self, name):
        club = Status.query.filter_by(club_name=name)
        if club.count() > 0:
            self.cs.many = False
            return self.ss.dump(club.first())
        return False

    def getClubsByCountry(self, country):
        clubs = Status.query.filter_by(club_country=country)
        if clubs.count() > 0:
            return self.ss.dump(clubs.all())
        return False


    def addClub(self, club):
        c = Status.query.filter_by(club_name=club.club_name)
        if c.count() > 0:
            return False, 'Club with the same name already exists'

        try:
            db.session.add(club)
            db.session.commit()
            self.cs.many=False
            return True, self.cs.dump(club)
        except Exception as ex:
            return False, str(ex)

    def sync_club_fb_status(self):
        cbl = ClubsBL()
        clubs = cbl.getClubsForSync()
        bl = StatusesBL()
        try:
            for club in clubs:
                statuses = get_posts(club.fb_link, page_limit=4, pages=10)
                for status in statuses:
                    bl.addClubSMStatus(club=club,socialMediaStatus=status)
            return True, 'Done'
        except Exception as e:
            return False, str(e)




