from ext import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    # დაამატე სხვა ველებიც, რაც გქონდა

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