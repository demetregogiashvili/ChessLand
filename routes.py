from flask import render_template, request, redirect, url_for
from models import User, Admin, Product, Orders
from ext import db, login_manager, app
from flask_login import current_user,login_user,logout_user,login_required
@app.route("/")
def index():
    return render_template("index.html",title = "home")
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email = email).first()
        if user:
            if user.password == password:
                login_user(user)
                return redirect("/")
            return redirect("/login")
        return redirect("/register")
    return render_template("login.html",title = "login")
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        username = request.form["username"]
        name = request.form["name"]
        surname = request.form["lastname"]
        img_url = request.form["img_url"]
        try:
            isAdmin = request.form.get("Admin", "noAdmin")
        except:
            isAdmin = "noAdmin"
        if User.query.filter_by(email = email).first():
            return render_template("register.html",title = "register",message = "Email already used")
        if User.query.filter_by(username = username).first():
            return render_template("register.html",title = "register",message = "username already used")

        user = User(
            username=username, password=password, name=name,
            surname=surname, email=email, profile_url=img_url,
            is_admin=(isAdmin == "Admin") # აქ ენიჭება True ან False
        )
        db.session.add(user)
        db.session.commit()
        if user.is_admin:
            user.is_admin = True
            new_admin = Admin(Adminname=username, Admin_id=user.id)
            db.session.add(new_admin)
            db.session.commit()
        return redirect("/login")
    return render_template("register.html",title = "register")
@app.route("/myclub")
def club():
    club = club.query.filter_by(Admin_id = current_user.id).first()
    print(club.clubname)
    return render_template("land.html",club = club)
# 1. პროდუქტის დამატების route
@app.route("/add_products", methods=['GET', 'POST'])
def addProduct():
    if request.method == "POST":
        title = request.form['title']
        picture = request.form['picture']
        price = request.form['price']  
        product = Product(title=title, img_url=picture, price=price, admin_id=current_user.id)
        db.session.add(product)
        db.session.commit()
        return redirect("/allproducts") # დამატების შემდეგ გადაიყვანს სიაში
    return render_template("add_products.html")

# 2. პროდუქტების სიის route
@app.route("/allproducts", methods=['GET'])
def products():
    all_products = Product.query.all()
    return render_template("all_products.html", products=all_products)
@app.route("/order/<int:product_id>", methods=['GET', 'POST'])
def makeOrder(product_id):
    if request.method == "POST":
        number = request.form["qountety"]
        date = request.form["date"]
        product = Product.query.get(product_id)
        order = Orders(
            number = number,
            date = date,
            product_id = product_id,
            user_id = current_user.id,
            admin_id = product.admin_id
        )
        db.session.add(order)
        db.session.commit()
    product = Product.query.get(product_id)
    return render_template("make_order.html",title = "make order",product = product)
@app.route("/delete_product/<int:product_id>")
@login_required
def delete_product(product_id):  
    if not current_user.is_admin:
        return "შენ არ გაქვს ადმინის უფლებები!", 403
    
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect("/allproducts") 
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))