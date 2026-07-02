from flask import Flask
from config import Config
from database import db
from models import *
from routes import coupon_bp

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
print("Database:", app.config["SQLALCHEMY_DATABASE_URI"])
print("Loaded tables:", db.metadata.tables.keys())
app.register_blueprint(coupon_bp)

@app.route("/")
def home():
    return {
        "message": "NativeWit Coupon System Running"
    }

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)