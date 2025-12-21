
from flask import Flask, render_template, request, redirect, url_for, session
import db

app = Flask(__name__)
app.secret_key = "inventory_secret"


@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    
    search = request.args.get("search", "")
    sort_by = request.args.get("sort", "")

    items = db.get_all_items()

    if search:
        items = [ item for item in items if search.lower() in item[1].lower() ]

    if sort_by == "name":
        items.sort(key = lambda x : x[1].lower())
    elif sort_by == "quantity":
        items.sort(key = lambda x : x[2])
    elif sort_by == "price":
        items.sort(key = lambda x : x[3])
        
    return render_template("inventory.html", items=items, search = search, sort_by = sort_by )

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["user"] = username
            return redirect(url_for("home"))
        else:
            error = "Invalid credentials"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/add", methods=["GET", "POST"])
def add():
    error = None

    if request.method == "POST":
        name = request.form.get("name")

        try:
            qty = int(request.form.get("qty"))
            price = float(request.form.get("price"))
        except (TypeError, ValueError):
            error = "Please enter valid values"
            return render_template("add.html", error=error)

        if not name or qty < 0 or price < 0:
            error = "Please enter valid values"
        else:
            db.add_item(name, qty, price)
            return redirect(url_for("home"))

    return render_template("add.html", error=error)
@app.route("/delete/<int:item_id>")
def delete(item_id):
    db.delete_item(item_id)
    return redirect(url_for("home"))

@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit(item_id):
    item = db.get_item_by_id(item_id)

    if request.method == "POST":
        name = request.form.get("name")
        qty = int(request.form.get("qty",0))
        price = float(request.form.get("price",0))

        db.update_item(item_id, name, qty, price)
        return redirect(url_for("home"))

    return render_template("edit.html", item=item)

if __name__ == "__main__":
    db.init_db()

from flask import Flask, render_template, request, redirect, url_for, session
import db

app = Flask(__name__)
app.secret_key = "inventory_secret"


@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    
    search = request.args.get("search", "")
    sort_by = request.args.get("sort", "")

    items = db.get_all_items()

    if search:
        items = [ item for item in items if search.lower() in item[1].lower() ]

    if sort_by == "name":
        items.sort(key = lambda x : x[1].lower())
    elif sort_by == "quantity":
        items.sort(key = lambda x : x[2])
    elif sort_by == "price":
        items.sort(key = lambda x : x[3])
        
    return render_template("inventory.html", items=items, search = search, sort_by = sort_by )

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":
            session["user"] = username
            return redirect(url_for("home"))
        else:
            error = "Invalid credentials"

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/add", methods=["GET", "POST"])
def add():
    error = None

    if request.method == "POST":
        name = request.form.get("name")

        try:
            qty = int(request.form.get("qty"))
            price = float(request.form.get("price"))
        except (TypeError, ValueError):
            error = "Please enter valid values"
            return render_template("add.html", error=error)

        if not name or qty < 0 or price < 0:
            error = "Please enter valid values"
        else:
            db.add_item(name, qty, price)
            return redirect(url_for("home"))

    return render_template("add.html", error=error)
@app.route("/delete/<int:item_id>")
def delete(item_id):
    db.delete_item(item_id)
    return redirect(url_for("home"))

@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit(item_id):
    item = db.get_item_by_id(item_id)

    if request.method == "POST":
        name = request.form.get("name")
        qty = int(request.form.get("qty",0))
        price = float(request.form.get("price",0))

        db.update_item(item_id, name, qty, price)
        return redirect(url_for("home"))

    return render_template("edit.html", item=item)

if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)