from flask import render_template, request, redirect
from models import User, ChessClub, Product, Orders
from ext import db, login_manager
from flask_login import current_user, login_user, logout_user, login_required

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
        return redirect("/login")
    return render_template("login.html", title="Login")

def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["username"]
        name = request.form["name"]
        surname = request.form["lastname"]
        img_url = request.form["img_url"]
        
        # ვამოწმებთ isAdmin ჩექბოქსს
        is_admin_check = request.form.get("isAdmin", "noadmin")
        
        if User.query.filter_by(email=email).first():
            return render_template("register.html", title="Register", message="Email already used")
        
        user = User(
            username=username, password=password, name=name,
            surname=surname, email=email, profile_url=img_url
        )
        db.session.add(user)
        db.session.commit()
        
        if is_admin_check == "admin":
            user.is_admin = True
            club = ChessClub(club_name=username, admin_id=user.id)
            db.session.add(club)
            db.session.commit()
            
        return redirect("/login")
    return render_template("register.html", title="Register")

def myclub():
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
    products = Product.query.all()
    return render_template("all_products.html", products=products)

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
            club_id=product.club.id
        )
        db.session.add(order)
        db.session.commit()
    product = Product.query.get(product_id)
    return render_template("make_order.html", title="Make Order", product=product)

@login_required
def singout():
    logout_user()
    return redirect("/")