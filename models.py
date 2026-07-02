from database import db
from datetime import datetime


# ----------------------------
# User Table
# ----------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)


# ----------------------------
# Coupon Table
# ----------------------------
class Coupon(db.Model):
    __tablename__ = "coupons"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=True)


# ----------------------------
# Coupon Usage Table
# ----------------------------
class CouponUsage(db.Model):
    __tablename__ = "coupon_usage"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    coupon_id = db.Column(db.Integer, db.ForeignKey("coupons.id"), nullable=False)

    used_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "coupon_id",
            name="unique_coupon_per_user"
        ),
    )


# ----------------------------
# Transaction Table
# ----------------------------
class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    coupon_id = db.Column(db.Integer, db.ForeignKey("coupons.id"), nullable=False)

    original_amount = db.Column(db.Float, nullable=False)
    discount = db.Column(db.Float, nullable=False)
    final_amount = db.Column(db.Float, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)