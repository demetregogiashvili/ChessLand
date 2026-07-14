from flask import Flask
from ext import db, login_manager
from models import User
from routes import index, login, register, view_myclub, addProduct, products, makeOrder, singout

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///ChessLand.db"
app.config["SECRET_KEY"] = "1234"

db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

app.add_url_rule("/", "index", index)
app.add_url_rule("/login", "login", login, methods=["GET", "POST"])
app.add_url_rule("/register", "reg", register, methods=["GET", "POST"])
app.add_url_rule("/logout", "logout", singout)
app.add_url_rule("/myclub", "myclub", view_myclub)
app.add_url_rule("/add_product/<club_id>", "addProduct", addProduct, methods=["GET", "POST"])
app.add_url_rule("/allproduct", "products", products)
app.add_url_rule("/order/<product_id>", "makeorder", makeOrder, methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")