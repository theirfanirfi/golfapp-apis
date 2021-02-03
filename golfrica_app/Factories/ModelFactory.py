from golfrica_app.Models.models import *


class MF:
    @staticmethod
    def getModel(blName):
        if blName == "status":
            return Status()
        elif blName == "club":
            return Club()
        elif blName == "club_description":
            return ClubDescription()
        elif blName == "rating":
            return Rating()
        elif blName == "swap":
            return Swap()
        elif blName == "user":
            return User()
        elif blName == "player":
            return Player()
        elif blName == "like":
            return Like()
        elif blName == "comment":
            return Comment()
        elif blName == "follow":
            return Follow()
        elif blName == "country":
            return Country()
        elif blName == "messages":
            return Messages()
        elif blName == "participant":
            return ChatParticipants()
        elif blName == "device":
            return LoginDevice()