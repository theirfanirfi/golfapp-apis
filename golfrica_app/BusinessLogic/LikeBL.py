from golfrica_app.Models.models import Like, LikeSchema
from datetime import datetime
from golfrica_app import db
import json
from golfrica_app.CoreClasses.Escape import *
from sqlalchemy import text
from flask import jsonify
class LikeBL:
    ss = LikeSchema(many=True)

    def likeStatus(self,user, status):
        isLikeAlready = Like.query.filter_by(is_status=1, user_id=user.user_id, status_id=status.status_id)
        if isLikeAlready.count() > 0:
            return False, 'Status is already liked', 'info'
        like = Like()
        like.is_status = 1
        like.user_id = user.user_id
        like.status_id = status.status_id
        like.created_at = str(datetime.now())[:10]
        like.updated_at = str(datetime.now())[:10]
        try:
            db.session.add(like)
            db.session.commit()
            return True, self.getStatusAppLikes(status.status_id), 'success'
        except Exception as e:
            return False, str(e), 'error'

    def unLikeStatus(self,user, status):
        like = Like.query.filter_by(is_status=1, user_id=user.user_id, status_id=status.status_id)
        if not like.count() > 0:
            return False, 'Status is not liked by you', 'info'
        like = like.first()
        try:
            db.session.delete(like)
            db.session.commit()
            return True, 'Status unliked', 'success'
        except Exception as e:
            return False, str(e), 'error'

    def getStatusAppLikes(self, status_id):
        return Like.query.filter_by(status_id=status_id).count()










