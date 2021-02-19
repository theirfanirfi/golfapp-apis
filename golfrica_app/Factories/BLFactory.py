from golfrica_app.BusinessLogic.ClubsBL import *
from golfrica_app.BusinessLogic.StatusesBL import *
from golfrica_app.BusinessLogic.RatingBL import *
from golfrica_app.BusinessLogic.SwapBL import *
from golfrica_app.BusinessLogic.PlayerBL import *
from golfrica_app.BusinessLogic.LikeBL import *
from golfrica_app.BusinessLogic.FollowBL import *
from golfrica_app.BusinessLogic.CountriesBL import *
from golfrica_app.BusinessLogic.CommentBL import *
from golfrica_app.BusinessLogic.UsersBL import *
from golfrica_app.BusinessLogic.ChatBL import *
from golfrica_app.BusinessLogic.ParticipantBL import *
from golfrica_app.BusinessLogic.NotificationBL import NotificationBL


class BL:
    @staticmethod
    def getBL(blName):
        if blName == "status":
            return StatusesBL()
        elif blName == "club":
            return ClubsBL()
        elif blName == "rating":
            return RatingBL()
        elif blName == "swap":
            return SwapBL()
        elif blName == "user":
            return UsersBL()
        elif blName == "player":
            return PlayerBL()
        elif blName == "like":
            return LikeBL()
        elif blName == "comment":
            return CommentBL()
        elif blName == "follow":
            return FollowBL()
        elif blName == "country":
            return CountryBL()
        elif blName == "chat":
            return ChatBL()
        elif blName == "participant":
            return ParticipantBL()
        elif blName == "notification":
            return NotificationBL()
