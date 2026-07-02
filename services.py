import logging
from database import db
from models import Coupon, CouponUsage, Transaction


def apply_coupon(user_id, coupon_code, amount):
    try:
        # Find active coupon
        coupon = (
            Coupon.query
            .filter_by(code=coupon_code, active=True)
            .with_for_update()
            .first()
        )

        if not coupon:
            return {
                "success": False,
                "message": "Coupon not found or inactive"
            }, 404

        # Check if user already used this coupon
        already_used = (
            CouponUsage.query
            .filter_by(
                user_id=user_id,
                coupon_id=coupon.id
           )
           .with_for_update()
           .first()
       )

        if already_used:
            return {
                "success": False,
                "message": "Coupon already used"
            }, 409

        # 100% discount
        discount = amount
        final_amount = 0

        # Create transaction
        transaction = Transaction(
            user_id=user_id,
            coupon_id=coupon.id,
            original_amount=amount,
            discount=discount,
            final_amount=final_amount
        )

        db.session.add(transaction)

        # Mark coupon as used
        usage = CouponUsage(
            user_id=user_id,
            coupon_id=coupon.id
        )

        db.session.add(usage)

        db.session.commit()

        return {
            "success": True,
            "message": "Coupon applied successfully",
            "transaction": {
                "id": transaction.id,
                "user_id": user_id,
                "coupon": coupon.code,
                "discount": discount,
                "final_amount": final_amount
          }
        }, 200

    except Exception as e:
        db.session.rollback()

        logging.exception(e)

        return {
            "success": False,
            "message": "Internal Server Error"
        }, 500