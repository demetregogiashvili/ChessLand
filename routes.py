from flask import render_template, request, redirect 
from ext import db 
from models import User, ChessClub 
def register():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["username"]

        # ვამოწმებთ, არსებობს თუ არა უკვე ეს მეილი
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "ეს მეილი უკვე დარეგისტრირებულია! სცადე სხვა."

        # თუ არ არსებობს, ვქმნით ახალ მომხმარებელს
        user = User(username=username, password=password, email=email, name=username)
        db.session.add(user)
        db.session.commit()

        if request.form.get("isAdmin") == "admin":
            club = ChessClub(club_name=username, admin_id=user.id)
            db.session.add(club)
            db.session.commit()
            
        return redirect("/login")
    return render_template("register.html", title="Register")

def index():
    return render_template("index.html")

def login():
    return render_template("login.html")

def view_myclub():
    return render_template("club.html")

def addProduct():
    return render_template("make_order.html") # ან შენი შესაბამისი გვერდი

def products():
    return render_template("product_card.html")

def makeOrder():
    return render_template("make_order.html")

def singout():
    return redirect("/")