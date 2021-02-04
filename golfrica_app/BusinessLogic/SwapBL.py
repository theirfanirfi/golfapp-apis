from golfrica_app.Models.models import Swap, SwapSchema
from datetime import datetime
from golfrica_app import db
from sqlalchemy import text
from golfrica_app.Factories.SchemaFactory import SF


class SwapBL:
    ss = SwapSchema(many=True)

    def swapStatus(self, user, status, swap_with=None):
        swaped_with = 0
        if status.is_app_status == 1:
            swaped_with = status.user_id if swap_with is None else swap_with.user_id
        elif status.is_club_status == 1:
            swaped_with = swap_with.user_id
        elif status.is_player_status == 1:
            swaped_with = swap_with.user_id
        else:
            return False, 'Invalid status', 'error'

        isAlreadySwapped, swap = self.getSwap(user, status, swaped_with)
        if isAlreadySwapped:
            return False, 'The status is already swaped', 'info'
        swap = Swap()
        swap.status_id = status.status_id
        swap.swaper_id = user.user_id
        swap.swaped_with_id = swaped_with
        swap.is_status = 1
        swap.created_at = str(datetime.now())
        swap.updated_at = str(datetime.now())
        try:
            db.session.add(swap)
            db.session.commit()
            return True, 'Swap request sent', 'success'
        except Exception as e:
            return False, str(e), 'error'

    def getSwap(self, user, status, swaped_with):
        swap = Swap.query.filter_by(swaper_id=user.user_id, status_id=status.status_id,
                                    swaped_with_id=swaped_with)
        if swap.count() > 0:
            return True, swap.first()
        else:
            return False, 'Swap not found'

    def getSwapNotifications(self, user):
        sql = text("SELECT swaps.*, "
                   "users.first_name, "
                   "users.last_name, "
                   "users.profile_image, "
                   "count(swap_id) as swap_requests "
                   "FROM swaps "
                   "LEFT JOIN users on users.user_id = swaps.swaper_id "
                   "WHERE swaped_with_id = " + str(user.user_id) + " GROUP BY swaps.swap_id")
        swaps = db.engine.execute(sql)
        if swaps.rowcount > 0:
            return True, self.ss.dump(swaps)
        else:
            return False, 'Swap not found'

    def getSwapObjectById(self, swap_id):
        swap = Swap.query.filter_by(swap_id=swap_id)
        if swap.count() > 0:
            return swap.first()
        else:
            return False

    def approveSwap(self, user, swap):
        if not user.user_id == swap.swaped_with_id:
            return False, 'The swap does not belong to you', 'error'

        swap.is_accepted = 1
        swap.updated_at = str(datetime.now())[:19]

        try:
            db.session.add(swap)
            db.session.commit()
            return True, 'Swap Approved', 'success'
        except:
            return False, 'Error occurred in approving the swap, please try again.', 'error'

    def declineSwap(self, user, swap):
        if not user.user_id == swap.swaped_with_id:
            return False, 'The swap does not belong to you', 'error'

        swap.is_rejected = 1
        swap.updated_at = str(datetime.now())[:19]

        try:
            db.session.add(swap)
            db.session.commit()
            return True, 'Swap declined', 'success'
        except:
            return False, 'Error occurred in declined the swap, please try again.', 'error'

    def getSwaps(self, user):
        current_time = str(datetime.now().strftime("%Y-%m-%d %H:%M:%S %p"))
        sql = text("SELECT statuses.*,swaps.*, clubs.club_id as cclub_id, clubs.club_name , clubs.club_profile_pic, players.player_id, players.player_name, players.player_profile_pic, "
                   + "JSON_OBJECT('swaper_id',swaper.user_id, 'swaper_name', CONCAT(swaper.first_name,' ', swaper.last_name), 'swaper_profile_pic', swaper.profile_image) as swaper_obj,"
                   + "JSON_OBJECT('poster_id',poster.user_id, 'poster_name', CONCAT(poster.first_name,' ', poster.last_name), 'poster_profile_pic', poster.profile_image) as poster_obj,"
                   + " JSON_OBJECT('swaped_with_id',swaped_with.user_id, 'swaped_with_name', CONCAT(swaped_with.first_name,' ', swaped_with.last_name), 'swaped_with_profile_pic', swaped_with.profile_image) as swaped_with_obj, "
                   + "time_to_sec(timediff('" + current_time + "',swaps.updated_at))/60 as timer, "
                   + "IF(swaps.swaper_id = " + str(user.user_id) + ",true,false) as isMe, "
                   + "swaps.updated_at as swap_time, statuses.created_at as status_posting_time, "
                   + "(select count(*) from likes WHERE status_id = statuses.status_id) as total_likes,"
                   + "(select count(*) from comments WHERE status_id = statuses.status_id) as total_comments,"
                   + "(select count(*) from swaps WHERE status_id = statuses.status_id) as total_swaps, "
                   + "(select avg(rating) from comments WHERE status_id = statuses.status_id) as avg_rating"
                   + " FROM swaps "
                   + "LEFT JOIN statuses on statuses.status_id = swaps.status_id"
                   + " LEFT JOIN users as swaper on swaper.user_id = swaps.swaper_id"
                   + " LEFT JOIN users as swaped_with on swaped_with.user_id = swaps.swaped_with_id"
                   + " LEFT JOIN clubs on clubs.club_id = statuses.club_id"
                   + " LEFT JOIN players on players.player_id = swaps.player_id "
                   + " LEFT JOIN users as poster on poster.user_id = statuses.user_id "
                   + " where (swaps.swaper_id = " + str(user.user_id)
                   + " and time_to_sec(timediff('" + current_time + "',swaps.updated_at))/60 < 1440 and is_accepted = 1 and is_reviewed = 0) "
                   + "or (swaped_with_id = " + str(user.user_id)
                   + " and time_to_sec(timediff('" + current_time + "',swaps.updated_at))/60 < 1440 and is_accepted = 1 and is_reviewed = 0)")
        swaps = db.engine.execute(sql)
        swaps = SF.getSchema("status").dump(swaps)
        return swaps
