from ext import db
from flask_login import UserMixin
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String,unique = True,nullable = False)
    password = db.Column(db.String,nullable = False)
    name = db.Column(db.String,nullable = False)
    surname = db.Column(db.String,nullable = False)
    email = db.Column(db.Integer,unique = True)
    profile_url = db.Column(db.String)
    is_admin = db.Column(db.Boolean,default = False)
    is_admin = db.relationship(
        "Admins",
        backref = "Admin"
    )
    orders = db.relationship(
        "Orders",
        backref = "user"
    )
class Admin(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    Adminname = db.Column(db.String)
    Admin_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    products = db.relationship(
        "Product",
        backref = "Admin"
    )
    orders = db.relationship(
        "Orders",
        backref = "Admin"
    )
class Product(db.Model):
    id = db.Column(db.Integer,primary_key= True)
    title = db.Column(db.String)
    img_url = db.Column(db.String)
    farm_id = db.Column(db.Integer, db.ForeignKey("admin.id")) 
    orders = db.relationship("Orders", backref="product")
class Orders(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    number = db.Column(db.Integer)
    date = db.Column(db.String)
    product_id = db.Column(db.Integer,db.ForeignKey("product.id"))
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))
    farm_id = db.Column(db.Integer,db.ForeignKey("farms.id"))