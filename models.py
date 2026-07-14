from ext import db
from flask_login import UserMixin

class User(db.Model, UserMixin): # აქ გაქვს ყველაფერი ერთად
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String(150), unique=True)
    profile_url = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)

class ChessClub(db.Model):
    __tablename__ = "chess_clubs"
    id = db.Column(db.Integer, primary_key=True)
    club_name = db.Column(db.String)
    admin_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    products = db.relationship("Product", backref="club")

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    img_url = db.Column(db.String)
    club_id = db.Column(db.Integer, db.ForeignKey("chess_clubs.id"))

class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String)
    date = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    club_id = db.Column(db.Integer, db.ForeignKey("chess_clubs.id"))