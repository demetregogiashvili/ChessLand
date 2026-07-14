from flask import render_template, request, redirect
from models import User, Product, Orders, ChessClub
from ext import db
from flask_login import current_user, login_user, logout_user

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
    return render_template("register.html")

def view_myclub():
    club = ChessClub.query.filter_by(admin_id=current_user.id).first()
    return render_template("club.html", club=club)