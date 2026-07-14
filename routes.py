from flask import render_template, request, redirect
from models import User, Product, Orders, ChessClub
from ext import db
from flask_login import current_user, login_user, logout_user

def index():
    return render_template("index.html", title="Home")

def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect("/")
    return render_template("login.html", title="Login")

def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["username"]
        
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        
        if request.form.get("isAdmin") == "admin":
            club = ChessClub(club_name=username, admin_id=user.id)
            db.session.add(club)
            db.session.commit()
            
        return redirect("/login")
    return render_template("register.html", title="Register")

def view_myclub():
    club = ChessClub.query.filter_by(admin_id=current_user.id).first()
    return render_template("club.html", club=club)

def addProduct(club_id):
    if request.method == "POST":
        title = request.form['title']
        picture = request.form["picture"]
        product = Product(title=title, img_url=picture, club_id=club_id)
        db.session.add(product)
        db.session.commit()
    return render_template("club_addproduct.html")

def products():
    all_products = Product.query.all()
    return render_template("all_products.html", products=all_products)

def makeOrder(product_id):
    if request.method == "POST":
        number = request.form["qountety"]
        date = request.form["date"]
        product = Product.query.get(product_id)
        order = Orders(
            number=number,
            date=date,
            product_id=product_id,
            user_id=current_user.id,
            club_id=product.club_id
        )
        db.session.add(order)
        db.session.commit()
    product = Product.query.get(product_id)
    return render_template("make_order.html", title="Make Order", product=product)

def singout():
    logout_user()
    return redirect("/")