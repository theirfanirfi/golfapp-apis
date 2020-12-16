from golfrica_app.Models.models import Follow, FollowSchema
from datetime import datetime
from golfrica_app import db
from golfrica_app.BusinessLogic.ClubsBL import ClubsBL
from sqlalchemy import or_, text

class FollowBL:
    fs = FollowSchema(many=True)
    cbl = ClubsBL()

    def followClub(self, user, club):
        follow = self.checkUserHasFollowedClub(user, club)
        if follow:
            try:
                db.session.delete(follow)
                db.session.commit()
                return True, 'Club unfollowed', 'success'
            except:
                return False, 'error occurred in unfollowing the club', 'error'

        follow = Follow()
        follow.is_club_followed = 1
        follow.followed_id = club.club_id
        follow.follower_id = user.user_id

        try:
            db.session.add(follow)
            db.session.commit()
            return True, 'Club Followed', 'success'
        except:
            return False, 'Error occurred in following the club', 'error'

    def followPlayer(self, user, player):
        follow = self.checkUserHasFollowedPlayer(user, player)
        if follow:
            try:
                db.session.delete(follow)
                db.session.commit()
                return False, 'Player unfollowed', 'success'
            except:
                return False, 'error occurred in unfollowing the player', 'error'

        follow = Follow()
        follow.is_player_followed = 1
        follow.followed_id = player.player_id
        follow.follower_id = user.user_id

        try:
            db.session.add(follow)
            db.session.commit()
            return True, 'Player Followed', 'success'
        except:
            return False, 'Error occurred in following the player.', 'error'

    def followUser(self, user, user_to_follow):
        follow = self.checkUserHasFollowedUser(user, user_to_follow)
        if follow:
            try:
                db.session.delete(follow)
                db.session.commit()
                return True, 'User unfollowed', 'success'
            except:
                return False, 'error occurred in unfollowing the user', 'error'

        follow = Follow()
        follow.is_user_followed = 1
        follow.followed_id = user_to_follow.user_id
        follow.follower_id = user.user_id

        try:
            db.session.add(follow)
            db.session.commit()
            return True, 'User Followed', 'success'
        except:
            return False, 'Error occurred in following the user', 'error'

    def checkUserHasFollowedClub(self, user, club):
        follow = Follow.query.filter_by(follower_id=user.user_id, followed_id=club.club_id, is_club_followed=1)
        if follow.count() > 0:
            return follow.first()
        return False

    def checkUserHasFollowedPlayer(self, user, player):
        follow = Follow.query.filter_by(follower_id=user.user_id, followed_id=player.player_id, is_player_followed=1)
        if follow.count() > 0:
            return follow.first()
        return False

    def checkUserHasFollowedUser(self, user, user_to_follow):
        follow = Follow.query.filter_by(follower_id=user.user_id, followed_id=user_to_follow.user_id, is_user_followed=1)
        if follow.count() > 0:
            return follow.first()
        return False

    def getClubFollowers(self, club_id):
        sql = text("SELECT *, count(follows.f_id) as total_followers FROM follows WHERE followed_id = '"+str(club_id)+"' AND is_club_followed = 1")
        club_followers = db.engine.execute(sql)
        return club_followers

    def getClubFollowersForTab(self, user, club_id):
        sql = text("SELECT follows.*, users.first_name, users.last_name, users.profile_image, users.user_id, "
                   "IF(follows.follower_id='"+str(user.user_id)+"', true, false) as is_followed,"
                                                                " (select count(f_id) FROM follows WHERE followed_id = users.user_id) as user_followers,"
                                                                " (select count(f_id) FROM follows WHERE follower_id = users.user_id) as users_followed "
                   "FROM follows "
                   "LEFT JOIN users on users.user_id = follows.follower_id "
                   "WHERE follows.followed_id = '"+str(club_id)+"' AND is_club_followed = 1")
        club_followers = db.engine.execute(sql)
        club_followers = self.fs.dump(club_followers)
        return club_followers






