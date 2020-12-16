from golfrica_app.Models.models import Player, PlayerSchema
from datetime import datetime
from golfrica_app import db
from sqlalchemy import or_, text

class PlayerBL:
    ps = PlayerSchema(many=True)

    def getPlayers(self, user, club):
        sql = text("SELECT *, avg(ratings.rating) as avg_rating, "
                   "count(ratings.rating_id) as total_reviews, "
                   "count(follows.f_id) as followers, IF(follows.follower_id = "+str(user.user_id)+", true, false) as is_followed "
                   "FROM players LEFT JOIN ratings on ratings.player_id = players.player_id "
                   "LEFT JOIN follows on follows.followed_id = players.player_id AND is_player_followed = 1 "
                   "WHERE players.club_id = "+str(club.club_id)+" GROUP BY players.player_id, ratings.rating_id, follows.f_id")
        players= db.engine.execute(sql)
        return self.ps.dump(players)

    def getClubsForSync(self):
        players= Player.query.all()
        return players

    def getClubById(self, id):
        player = Player.query.filter_by(club_id=id)
        if player.count() > 0:
            self.ps.many = False
            return self.ps.dump(player.first())
        return False


    def getPlayerObjById(self, id):
        player = Player.query.filter_by(player_id=id)
        if player.count() > 0:
            return player.first()
        return False







