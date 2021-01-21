from golfrica_app.Models.models import (
    Messages,
    ChatParticipants,
    User,
    Player,
    Club,
    ClubDescription,
    Comment,
    Like,
    Rating,
    Swap,
    Status,
    Follow,
    Country,
    Messages,
)


class MF:
    @staticmethod
    def getSchema(blName):
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