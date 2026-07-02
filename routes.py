from flask import Blueprint, request, jsonify
from models import Coupon, CouponUsage
from services import apply_coupon

coupon_bp = Blueprint("coupon", __name__)

@coupon_bp.route("/validate-coupon", methods=["POST"])
def validate_coupon():

    data = request.get_json()

    user_id = data["user_id"]
    coupon_code = data["coupon"]
    amount = data["amount"]

    coupon = Coupon.query.filter_by(
        code=coupon_code,
        active=True
    ).first()

    if not coupon:
        return jsonify({
            "valid": False,
            "message": "Coupon not found or inactive"
        }), 400

    already_used = CouponUsage.query.filter_by(
        user_id=user_id,
        coupon_id=coupon.id
    ).first()

    if already_used:
        return jsonify({
            "valid": False,
            "message": "Coupon already used"
        }), 400

    return jsonify({
        "valid": True,
        "discount": amount,
        "final_amount": 0
    })

@coupon_bp.route("/apply-coupon", methods=["POST"])
def apply_coupon_route():

    data = request.get_json()

    user_id = data["user_id"]
    coupon_code = data["coupon"]
    amount = data["amount"]

    response, status = apply_coupon(
        user_id,
        coupon_code,
        amount
    )

    return jsonify(response), status
