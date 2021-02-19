from golfrica_app.Models.models import *


class SF:
    @staticmethod
    def getSchema(blName, isMany=True):
        if blName == "status":
            return StatusSchema(many=isMany)
        elif blName == "club":
            return ClubSchema(many=isMany)
        elif blName == "club_description":
            return ClubDesSchema(many=isMany)
        elif blName == "rating":
            return RatingSchema(many=isMany)
        elif blName == "swap":
            return SwapSchema(many=isMany)
        elif blName == "user":
            return UserSchema(many=isMany)
        elif blName == "player":
            return PlayerSchema(many=isMany)
        elif blName == "like":
            return LikeSchema(many=isMany)
        elif blName == "comment":
            return CommentSchema(many=isMany)
        elif blName == "follow":
            return FollowSchema(many=isMany)
        elif blName == "country":
            return CountrySchema(many=isMany)
        elif blName == "chat":
            return ChatSchema(many=isMany)
        elif blName == "participant":
            return ChatSchema(many=isMany)
        elif blName == "device":
            return LoginDeviceSchema(many=isMany)
        elif blName == "notification":
            return NotificationSchema(many=isMany)