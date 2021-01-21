from golfrica_app.Models.models import (
    Status,
    StatusSchema,
    Club,
    Like,
    LikeSchema,
    Comment,
    CommentSchema,
)
from datetime import datetime
from golfrica_app import db
import json
from golfrica_app.CoreClasses.Escape import *
from sqlalchemy import text
from flask import jsonify


class StatusesBL:
    ss = StatusSchema(many=True)

    def getAppStatuses(self):
        statuses = Status.query.join(Club, (Club.club_id == Status.club_id)).all()
        return self.ss.dump(statuses)

    def getStatusesForFeed(self, user, offset):
        user_id = str(user.user_id)
        print(offset)
        sql = text(
            "(SELECT statuses.*, clubs.club_name, clubs.club_profile_pic, (select count(*) from likes WHERE status_id = statuses.status_id) as total_likes,  (select count(*) from swaps WHERE status_id = statuses.status_id) as total_swaps,  (select count(*) from comments WHERE status_id = statuses.status_id) as total_comments, (select avg(rating) from comments WHERE status_id = statuses.status_id) as avg_rating FROM follows LEFT JOIN statuses on statuses.`club_id` = follows.`followed_id` LEFT JOIN clubs on clubs.club_id = statuses.club_id WHERE follows.`is_club_followed` = 1 AND follows.`follower_id` = "
            + user_id
            + ") UNION (SELECT statuses.*, players.player_name, players.player_profile_pic, (select count(*) from likes WHERE status_id = statuses.status_id) as total_likes,  (select count(*) from swaps WHERE status_id = statuses.status_id) as total_swaps, (select count(*) from comments WHERE status_id = statuses.status_id) as total_comments, (select avg(rating) from comments WHERE status_id = statuses.status_id) as avg_rating FROM follows LEFT JOIN statuses on statuses.`player_id` = follows.`followed_id` LEFT JOIN players on players.player_id = statuses.player_id WHERE follows.`is_player_followed` = 1 AND follows.`follower_id` = "
            + user_id
            + ") UNION (SELECT statuses.*, users.first_name, users.`profile_image`, (select count(*) from likes WHERE status_id = statuses.status_id) as total_likes,  (select count(*) from swaps WHERE status_id = statuses.status_id) as total_swaps, (select count(*) from comments WHERE status_id = statuses.status_id) as total_comments, (select avg(rating) from comments WHERE status_id = statuses.status_id) as avg_rating FROM follows LEFT JOIN statuses on statuses.`user_id` = follows.`followed_id` LEFT JOIN users on users.user_id = statuses.user_id WHERE follows.`is_user_followed` = 1 AND follows.`follower_id` = "
            + user_id
            + ") UNION (SELECT statuses.*, users.first_name, users.`profile_image`, (select count(*) from likes WHERE status_id = statuses.status_id) as total_likes, (select count(*) from swaps WHERE status_id = statuses.status_id) as total_swaps,(select count(*) from comments WHERE status_id = statuses.status_id) as total_comments, (select avg(rating) from comments WHERE status_id = statuses.status_id) as avg_rating FROM statuses LEFT JOIN users on users.user_id = statuses.user_id WHERE statuses.user_id = "
            + user_id
            + ") ORDER BY status_id DESC LIMIT 10 OFFSET "
            + str(offset)
        )
        statuses = db.engine.execute(sql)
        return self.ss.dump(statuses)

    def getSMStatuses(self):
        sql = text(
            "SELECT *, "
            " (select count(*) from likes WHERE status_id = statuses.status_id) as total_likes, "
            "(select count(*) from comments WHERE status_id = statuses.status_id) as total_comments, "
            "(select count(*) from swaps WHERE status_id = statuses.status_id) as total_swaps, "
            "(select avg(rating) from comments WHERE status_id = statuses.status_id) as avg_rating  "
            "FROM statuses LEFT JOIN clubs on clubs.club_id = statuses.club_id WHERE is_sm_status = 1 and statuses.status_id > 184"
        )
        statuses = db.engine.execute(sql)
        return self.ss.dump(statuses)

    def getStatusById(self, id):
        status = Status.query.filter_by(status_id=id)
        if status.count() > 0:
            self.ss.many = False
            return self.ss.dump(status.first())
        return False

    def getClubStatuses(self, user, id, offset):
        sql = text(
            "SELECT statuses.*, clubs.club_name, clubs.club_profile_pic, (select count(*) from likes WHERE status_id = statuses.status_id) as total_likes, (select count(*) from likes WHERE status_id = statuses.status_id AND user_id = "
            + str(user.user_id)
            + ") as isLiked, (select count(*) from swaps WHERE status_id = statuses.status_id) as total_swaps, (select count(*) from comments WHERE status_id = statuses.status_id) as total_comments,(select avg(rating) from comments WHERE status_id = statuses.status_id) as avg_rating FROM statuses LEFT JOIN clubs on clubs.club_id = statuses.club_id WHERE statuses.club_id = "
            + str(id)
            + " ORDER BY statuses.status_id DESC LIMIT 20 OFFSET "
            + str(offset)
        )
        statuses = db.engine.execute(sql)
        return self.ss.dump(statuses)

    def getPlayerStatuses(self, user, id, offset):
        sql = text(
            "SELECT statuses.*,players.*, clubs.club_name, clubs.club_profile_pic, (select count(*) from likes WHERE status_id = statuses.status_id) as total_likes, (select count(*) from likes WHERE status_id = statuses.status_id AND user_id = "
            + str(user.user_id)
            + ") as isLiked, (select count(*) from swaps WHERE status_id = statuses.status_id) as total_swaps, (select count(*) from comments WHERE status_id = statuses.status_id) as total_comments, (select avg(rating) from comments WHERE status_id = statuses.status_id) as avg_rating FROM statuses LEFT JOIN players on players.player_id = statuses.player_id LEFT JOIN clubs on clubs.club_id = players.player_id WHERE statuses.player_id = "
            + str(id)
            + " ORDER BY statuses.status_id DESC LIMIT 20 OFFSET "
            + str(offset)
        )
        statuses = db.engine.execute(sql)
        return self.ss.dump(statuses)

    def getStatusByIdAsJsonDump(self, id):
        isFound, status = self.getStatusByIdObject(id)
        if not isFound:
            return False

        if status.is_app_status == 1:
            status = self.getStatusWithAppUserProfile(id)
            return self.ss.dump(status)
        elif status.is_club_status == 1:
            status = self.getStatusWithClubProfile(id)
            return self.ss.dump(status)
        elif status.is_player_status == 1:
            return self.getStatusWithPlayerProfile(id)
        else:
            return False

    def getStatusWithClubProfile(self, id):
        sql = text(
            "SELECT *, (select count(*) from likes WHERE status_id = statuses.status_id) as total_likes, "
            "(select count(*) from comments WHERE status_id = statuses.status_id) as total_comments, "
            "(select count(*) from swaps WHERE status_id = statuses.status_id) as total_swaps, "
            "(select avg(rating) from comments WHERE status_id = statuses.status_id) as avg_rating  "
            "FROM statuses LEFT JOIN clubs on clubs.club_id = statuses.club_id WHERE status_id = '"
            + str(id)
            + "'"
        )
        status = db.engine.execute(sql)
        return status

    def getStatusWithAppUserProfile(self, id):
        print("status id: " + id)
        sql = text(
            "SELECT *, (select count(*) from likes WHERE status_id = statuses.status_id) as total_likes, "
            "(select count(*) from comments WHERE status_id = statuses.status_id) as total_comments, "
            "(select count(*) from swaps WHERE status_id = statuses.status_id) as total_swaps, "
            "(select avg(rating) from comments WHERE status_id = statuses.status_id) as avg_rating  "
            "FROM statuses LEFT JOIN users on users.user_id = statuses.user_id WHERE status_id = '"
            + str(id)
            + "'"
        )
        status = db.engine.execute(sql)
        return status

    def getStatusWithPlayerProfile(self, id):
        pass

    def getStatusByIdObject(self, id):
        status = Status.query.filter_by(status_id=id)
        if status.count() > 0:
            return True, status.first()
        return False, False

    def mediaLinksToJson(self, media):
        data = {
            "video": media["video"],
            "images": media["images"],
        }
        return json.dumps(data)

    def addClubSMStatus(self, club, socialMediaStatus):
        status = Status()
        try:
            status.club_id = club.club_id
            status.is_club_status = 1
            status.is_sm_status = 1
            status.status_description = escape_string(
                strip_emoji(socialMediaStatus["post_text"])
            )
            status.status_link = escape_string(socialMediaStatus["post_url"])
            status.status_media = self.mediaLinksToJson(media=socialMediaStatus)
            status.status_sm_likes = socialMediaStatus["likes"]
            status.status_sm_comments = socialMediaStatus["comments"]
            status.status_sm_shares = socialMediaStatus["shares"]
            status.created_at = str(socialMediaStatus["time"])
            status.updated_at = str(datetime.now())[:10]
            db.session.add(status)
            db.session.commit()
            self.ss.many = False
            return True
        except Exception as ex:
            return False, str(ex)

    def addUserStatus(self, user, data):
        status = Status()
        try:
            status.is_app_status = 1
            status.user_id = user.user_id
            status.status_description = data["status"]
            status.status_media = self.mediaLinksToJson(media=data["media"])
            status.created_at = str(datetime.now())[:10]
            status.updated_at = str(datetime.now())[:10]
            db.session.add(status)
            db.session.commit()
            self.ss.many = False
            return True, self.ss.dump(status)
        except Exception as ex:
            return False, str(ex)
