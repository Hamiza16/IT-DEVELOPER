from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
import db
import math
import csv
from io import StringIO

app = Flask(__name__)
app.secret_key = "your_secret_key"


@app.route("/")
def home():
    if "user" not in session:
        return redirect(url_for("login"))
    
    search = request.args.get("search", "")
    sort_by = request.args.get("sort", "")

    items = db.get_all_items()

    page = int(request.args.get("page", 1))
    per_page = 5             
    total_items = len(items)
    total_pages = (total_items + per_page - 1) // per_page

    start = (page - 1) * per_page
    end = start + per_page
    items = items[start:end]

    if search:
        items = [ item for item in items if search.lower() in item[1].lower() ]

    if sort_by == "name":
        items.sort(key = lambda x : x[1].lower())
    elif sort_by == "quantity":
        items.sort(key = lambda x : x[2])
    elif sort_by == "price":
        items.sort(key = lambda x : x[3])
        
    return render_template("inventory.html", items=items, page=page, total_pages=total_pages, search = search, sort_by = sort_by )

@app.route("/export")
def export_csv():
    items = db.get_all_items()  # Assuming this returns list of tuples/lists

    # In-memory file
    si = StringIO()
    writer = csv.writer(si)

    # Header
    writer.writerow(["ID", "Name", "Quantity", "Price"])

    # Data rows
    for item in items:
        writer.writerow(item)

    # Create response
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=inventory.csv"
    output.headers["Content-type"] = "text/csv"

    return output
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
    flash("Logged out successfully!", "info")
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
            flash("Item added successfully!", "success")
            return redirect(url_for("home"))

    return render_template("add.html", error=error)
@app.route("/delete/<int:item_id>")
def delete(item_id):
    db.delete_item(item_id)
    flash("Item deleted successfully!", "success")
    return redirect(url_for("home"))

@app.route("/edit/<int:item_id>", methods=["GET", "POST"])
def edit(item_id):
    item = db.get_item_by_id(item_id)

    if request.method == "POST":
        name = request.form.get("name")
        qty = int(request.form.get("qty",0))
        price = float(request.form.get("price",0))

        db.update_item(item_id, name, qty, price)
        flash("Item updated successfully!", "success")
        return redirect(url_for("home"))

    return render_template("edit.html", item=item)

if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)

