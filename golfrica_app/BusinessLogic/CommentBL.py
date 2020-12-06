from golfrica_app.Models.models import Comment, CommentSchema
from datetime import datetime
from golfrica_app import db
from flask import escape, jsonify
from sqlalchemy import text
from golfrica_app.CoreClasses.Escape import escape_string
# from golfrica_app.BusinessLogic.StatusesBL import StatusesBL
class CommentBL:
    cs = CommentSchema(many=True)
    # sbl = StatusesBL()

    def commentStatus(self,user, status, comment, rating):
        com = Comment()
        com.is_status = 1
        com.user_id = user.user_id
        com.status_id = status.status_id
        com.comment = escape_string(comment)
        com.rating = rating
        com.created_at = str(datetime.now())[:10]
        com.updated_at = str(datetime.now())[:10]
        try:
            db.session.add(com)
            db.session.commit()
            return True, self.getCommentByIdWithUserDetails(com.comment_id), 'success'
        except Exception as e:
            return False, str(e), 'error'


    def deleteComment(self, comment):
        com = Comment.query.filter_by(comment_id=comment.comment_id)
        if not com.count() > 0:
            return False, 'Comment not found', 'error'

        try:
            db.session.delete(com)
            db.session.commit()
            return True, 'Commented', 'success'
        except Exception as e:
            return False, str(e), 'error'

    def getStatusComments(self, status_id):
        sql = text("SELECT * FROM comments LEFT JOIN users on users.user_id = comments.user_id WHERE status_id= '"+str(status_id)+"'")
        comments = db.engine.execute(sql)
        return ({'comments': [dict(row) for row in comments]})

    def getStatusCommentsWithClubProfile(self, status_id):
        pass
    def getStatusCommentsWithPlayerProfile(self, status_id):
        pass
    def getStatusCommentsWithAppUserProfile(self, status_id):
        pass

    def getCommentByIdWithUserDetails(self, comment_id):
        sql = text("SELECT * FROM comments LEFT JOIN users on users.user_id = comments.user_id WHERE comments.comment_id= '"+str(comment_id)+"'")
        comments = db.engine.execute(sql)
        return self.cs.dumps(comments)









