from golfrica_app.Models.models import Rating, RatingSchema
from datetime import datetime
from golfrica_app import db
from golfrica_app.BusinessLogic.ClubsBL import ClubsBL
from sqlalchemy import or_, text

class RatingBL:
    rs = RatingSchema(many=True)
    cbl = ClubsBL()

    def rateClub(self, user, club, data):
        rating = self.getUserRatingForClub(user, club)
        if not rating:
            rating = Rating()

        rating.user_id = user.user_id
        rating.rating = data['rating_stars']
        rating.review = data['review']
        rating.club_id = club.club_id
        rating.is_club_rating = 1

        try:
            db.session.add(rating)
            db.session.commit()
            return True, rating.rating, 'success'
        except:
            return False, 'Error occurred in rating the club', 'error'

    def getUserRatingForClub(self, user, club):
        rating = Rating.query.filter_by(user_id=user.user_id, club_id=club.club_id, is_club_rating=1)
        if rating.count() > 0:
            return rating.first()
        return False

    def getClubAverageRating(self, club_id):
        sql = text("SELECT avg(rating) as avg_rating, count(ratings.rating_id) as total_reviews FROM ratings WHERE club_id = '"+str(club_id)+"'")
        average_rating = db.engine.execute(sql)
        average_rating = average_rating.first()
        rating = []
        if average_rating[0] == None:
            rating.append(0)
        else:
            rating.append(average_rating[0])

        if average_rating[1] == None:
            rating.append(0)
        else:
            rating.append(average_rating[1])

        return rating






