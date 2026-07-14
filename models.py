from ext import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    surname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    profile_url = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)
    is_farmer = db.Column(db.Boolean, default=False)
    
    farm = db.relationship("Farms", backref="farmer")
    orders = db.relationship("Orders", backref="user")

class Farms(db.Model):
    __tablename__ = "farms"
    id = db.Column(db.Integer, primary_key=True)
    farmname = db.Column(db.String)
    farmer_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    products = db.relationship("Product", backref="farm")
    orders = db.relationship("Orders", backref="farm")

class Product(db.Model):
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    img_url = db.Column(db.String)
    farm_id = db.Column(db.Integer, db.ForeignKey("farms.id"))
    
    orders = db.relationship("Orders", backref="product")

class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    date = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    farm_id = db.Column(db.Integer, db.ForeignKey("farms.id"))