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
        user = User(username=username, password=password, email=email)
        db.session.add(user)
        db.session.commit()

        if request.form.get("isAdmin") == "admin":
            club = ChessClub(club_name=username, admin_id=user.id)
            db.session.add(club)
            db.session.commit()
            
        return redirect("/login")
    return render_template("register.html", title="Register")