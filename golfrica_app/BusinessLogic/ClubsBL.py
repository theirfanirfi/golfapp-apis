from golfrica_app.Models.models import Club, ClubSchema, ClubDesSchema
from datetime import datetime
from golfrica_app.Models.models import ClubDescription
from golfrica_app import db
from sqlalchemy import or_, text
from golfrica_app.Globals.ImageUpload import mediaLinksToJson


class ClubsBL:
    cs = ClubSchema(many=True)
    cds = ClubDesSchema(many=True)

    def getClubs(self, user):
        # sql = text("SELECT clubs.*, count(f_id) as followers, "
        #            "count(ratings.rating_id) as total_reviews, "
        #            "avg(ratings.rating) as avg_rating, IF(follows.follower_id = "+str(user.user_id)+", true, false) as is_followed "
        #            "FROM clubs LEFT JOIN follows on follows.followed_id = clubs.club_id AND follows.is_club_followed = 1 "
        #            "LEFT JOIN ratings on ratings.club_id = clubs.club_id "
        #            "GROUP BY clubs.club_id, follows.follower_id")
        sql = text("SELECT clubs.*, "
                   + "(select count(*) from follows WHERE followed_id = clubs.club_id AND is_club_followed =1) as followers,"
                   + "(select count(*) from ratings WHERE ratings.club_id = clubs.club_id) as total_reviews,"
                   + "(select avg(ratings.rating) from ratings WHERE ratings.club_id = clubs.club_id) as avg_rating,"
                   + "(select IF(follows.follower_id = " + str(
            user.user_id) + ", true, false) from follows WHERE follows.followed_id = clubs.club_id "
                   + "AND follows.follower_id = " + str(
            user.user_id) + " AND follows.`is_club_followed` = 1 ) as is_followed  FROM clubs ")
        clubs = db.engine.execute(sql)
        return self.cs.dump(clubs)

    def getClubsByCountryForTab(self, user, country_id):
        # sql = text("SELECT clubs.*, count(f_id) as followers, "
        #            "count(ratings.rating_id) as total_reviews, "
        #            "avg(ratings.rating) as avg_rating, IF(follows.follower_id = " + str(
        #     user.user_id) + ", true, false) as is_followed "
        #                     "FROM clubs LEFT JOIN follows on follows.followed_id = clubs.club_id AND follows.is_club_followed = 1 "
        #                     "LEFT JOIN ratings on ratings.club_id = clubs.club_id WHERE clubs.club_country=" + str(
        #     country_id) +
        #            " GROUP BY clubs.club_id, follows.follower_id")
        sql = text("SELECT clubs.*, "
                   + "(select count(*) from follows WHERE followed_id = clubs.club_id AND is_club_followed =1) as followers,"
                   + "(select count(*) from ratings WHERE ratings.club_id = clubs.club_id) as total_reviews,"
                   + "(select avg(ratings.rating) from ratings WHERE ratings.club_id = clubs.club_id) as avg_rating,"
                   + "(select IF(follows.follower_id = " + str(
            user.user_id) + ", true, false) from follows WHERE follows.followed_id = clubs.club_id "
                   + "AND follows.follower_id = " + str(
            user.user_id) + " AND follows.`is_club_followed` = 1 ) as is_followed  FROM clubs ")
        clubs = db.engine.execute(sql)
        return self.cs.dump(clubs)

    def getClubsForSync(self):
        clubs = Club.query.all()
        return clubs

    def getClubById(self, id):
        club = Club.query.filter_by(club_id=id)
        if club.count() > 0:
            self.cs.many = False
            return self.cs.dump(club.first())
        return False

    def getClubProfile(self, id, user):
        sql = text(
            "SELECT clubs.*, (select count(*) from follows where follows.followed_id = clubs.club_id AND follows.is_club_followed = 1 ) as followers, (select count(*) from follows where follows.followed_id = clubs.club_id AND follows.is_club_followed = 1 AND follows.follower_id = " + str(
                user.user_id) + ") as is_followed, (select count(*) from players where players.club_id = clubs.club_id) as players, (select count(*) from statuses where statuses.club_id = clubs.club_id) as total_statuses FROM clubs WHERE clubs.club_id = " + str(
                id))
        club = db.engine.execute(sql)
        if club.rowcount > 0:
            self.cs.many = False
            return self.cs.dump(club.first())
        return False

    def getClubDescriptionWithUsers(self, club_id):
        sql = text("select club_description.*, profile_image, first_name, last_name from club_description "
                   "left join users on users.user_id = club_description.user_id Where club_id = '" + str(
            club_id) + "' ORDER BY des_id DESC ")
        club_descriptions = db.engine.execute(sql)
        return self.cds.dump(club_descriptions)

    def getClubObjById(self, id):
        club = Club.query.filter_by(club_id=id)
        if club.count() > 0:
            return club.first()
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
            self.cs.many = False
            return True, self.cs.dump(club)
        except Exception as ex:
            return False, str(ex)

    def addClubDescriptoin(self, user, club_id, desc, media):
        club = self.getClubObjById(club_id)
        if not club:
            return False, 'Club not found', 'error'

        cd = ClubDescription()
        cd.club_id = club.club_id
        cd.user_id = user.user_id
        cd.des_text = desc
        cd.des_media = mediaLinksToJson(media['media'])

        try:
            db.session.add(cd)
            db.session.commit()
            return True, 'Club description updated', 'success'
        except:
            return False, 'Error occurred in updating club description', 'error'
