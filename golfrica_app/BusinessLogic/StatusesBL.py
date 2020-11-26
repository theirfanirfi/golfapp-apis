from golfrica_app.Models.models import Status, StatusSchema, Club, Like, LikeSchema,\
    Comment, CommentSchema
from datetime import datetime
from golfrica_app import db
import json
from golfrica_app.CoreClasses.Escape import *
from sqlalchemy import text
from flask import jsonify
class StatusesBL:
    ss = StatusSchema(many=True)

    def getAppStatuses(self):
        statuses= Status.query.join(Club, (Club.club_id==Status.club_id)).all()
        return self.ss.dump(statuses)

    def getSMStatuses(self):
        sql = text("SELECT *, (select count(*) from likes WHERE status_id = statuses.status_id) as total_likes, "
                   "(select count(*) from comments WHERE status_id = statuses.status_id) as total_comments, "
                   "(select count(*) from swaps WHERE status_id = statuses.status_id) as total_swaps "
                   "FROM statuses LEFT JOIN clubs on clubs.club_id = statuses.club_id WHERE is_sm_status = 1")
        statuses= db.engine.execute(sql)
        return self.ss.dump(statuses)

    def getStatusById(self, id):
        status = Status.query.filter_by(status_id=id)
        if status.count() > 0:
            self.ss.many = False
            return self.ss.dump(status.first())
        return False

    def getStatusByIdObject(self,id):
        status = Status.query.filter_by(status_id=id)
        if status.count() > 0:
            return True, status.first()
        return False, False

    def mediaLinksToJson(self, media):
        data = {
            'video': media['video'],
            'images': media['images'],
        }
        return escape_string(json.dumps(data))

    def addClubSMStatus(self, club, socialMediaStatus):
        status = Status()
        try:
            status.club_id = club.club_id
            status.is_club_status = 1
            status.status_description = strip_emoji(escape_string(socialMediaStatus['post_text']))
            status.status_link = escape_string(socialMediaStatus['post_url'])
            status.status_media = self.mediaLinksToJson(media=socialMediaStatus)
            status.status_sm_likes = socialMediaStatus['likes']
            status.status_sm_comments = socialMediaStatus['comments']
            status.status_sm_shares = socialMediaStatus['shares']
            status.created_at = str(socialMediaStatus['time'])
            status.updated_at = str(datetime.now())[:10]
            db.session.add(status)
            db.session.commit()
            self.ss.many=False
            return True
        except Exception as ex:
            return False, str(ex)










