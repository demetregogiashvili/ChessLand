from flask import Flask
from models import *
from ext import login_manager,db
from routes import *
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///FarmDB.db"
app.config["SECRET_KEY"] = "1234"
db.init_app(app)
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
with app.app_context():
    db.create_all()
app.add_url_rule("/","index",index)
app.add_url_rule("/login","login",login,methods = ["get","post"])
app.add_url_rule("/register","reg",register,methods = ["get","post"])
app.add_url_rule("/logout","logout",singout)
app.add_url_rule("/myclub", "club", club)
app.add_url_rule("/add_product/<farm_id>","addProduct",addProduct,methods = ["get","post"])
app.add_url_rule("/allproduct","products",products)
app.add_url_rule("/order/<product_id>","makeorder",makeOrder,methods = ["get","post"])
if __name__ == "__main__":
    app.run(debug = True,host="0.0.0.0")