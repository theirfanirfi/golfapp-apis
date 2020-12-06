from golfrica_app.Models.models import Swap, SwapSchema
from datetime import datetime
from golfrica_app import db
class SwapBL:
    ss = SwapSchema(many=True)

    def swapStatus(self, user, status):
        swaped_with = 0
        if status.is_app_status == 1:
            swaped_with = status.user_id
        elif status.is_club_status == 1:
            swaped_with = status.club_id
        elif status.is_player_status == 1:
            swaped_with = status.player_id
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










