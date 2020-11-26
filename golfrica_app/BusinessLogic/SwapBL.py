from golfrica_app.Models.models import Swap, SwapSchema
from datetime import datetime
from golfrica_app import db
class CommentBL:
    ss = SwapSchema(many=True)

    def swapStatus(self,user, status, swap_with_id):
        isAlreadySwapped, swap = self.getSwap(user, status, swap_with_id)
        if isAlreadySwapped:
            return False, 'The status is already swaped', 'info'
        swap = Swap()
        swap.status_id = status.status_id
        swap.swaper_id = user.user_id
        swap.swaped_with_id = swap_with_id
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










