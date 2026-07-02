from app import app
from database import db
from models import User, Coupon

with app.app_context():

    if not User.query.first():
        db.session.add(User(name="Vijin"))
        db.session.add(User(name="Rahul"))

    if not Coupon.query.filter_by(code="FREE100").first():
        db.session.add(Coupon(
            code="FREE100",
            active=True
        ))

    db.session.commit()

    print("Sample data inserted!")
