from flask import Flask, render_template, request, redirect, url_for, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "abcend-secret"

USERS = {
    "jameel": {"password": "admin123", "role": "Owner", "name": "Jameel"},
    "store": {"password": "1234", "role": "Store Keeper", "name": "Store Keeper"},
    "sales": {"password": "1234", "role": "Sales / Cashier", "name": "Sales"},
    "support": {"password": "1234", "role": "Customer Support", "name": "Support"},
    "delivery": {"password": "1234", "role": "Delivery / Dispatch", "name": "Delivery"},
    "account": {"password": "1234", "role": "Accountant", "name": "Accountant"},
}

PERMISSIONS = {
    "Owner": ["stock", "sales", "support", "delivery", "finance", "users"],
    "Store Keeper": ["stock"],
    "Sales / Cashier": ["sales"],
    "Customer Support": ["support"],
    "Delivery / Dispatch": ["delivery"],
    "Accountant": ["finance"],
}

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

def require_permission(page):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            role = session["user"]["role"]
            if page not in PERMISSIONS[role]:
                return render_template("denied.html", user=session["user"], page=page), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator

PRODUCTS = [
    {"name": "Volvo FH Air Filter", "cat": "Truck Parts", "qty": 12, "price": 45500},
    {"name": "Mack Truck Brake Pad", "cat": "Truck Parts", "qty": 4, "price": 62000},
    {"name": "Toyota Hiace Oil Filter", "cat": "Engine", "qty": 28, "price": 9800},
    {"name": "Iveco Clutch Plate", "cat": "Transmission", "qty": 2, "price": 88000},
    {"name": "Mercedes Actros Shock Absorber", "cat": "Suspension", "qty": 8, "price": 72500},
]

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form.get("username")
        p = request.form.get("password")
        if u in USERS and USERS[u]["password"] == p:
            session["user"] = USERS[u]
            return redirect(url_for("dashboard"))
        return render_template("login.html", error="Wrong username or password")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    low = [p for p in PRODUCTS if p["qty"] < 5]
    return render_template("dashboard.html", user=session["user"], products=PRODUCTS, low=low, perms=PERMISSIONS[session["user"]["role"]])

@app.route("/stock")
@login_required
@require_permission("stock")
def stock():
    return render_template("page.html", user=session["user"], title="Stock Management", desc="Stock In/Out, Adjust Inventory, Stock Report")

@app.route("/sales")
@login_required
@require_permission("sales")
def sales():
    return render_template("page.html", user=session["user"], title="Sales & Invoices", desc="Create Invoice, Receipts, Cash & Bank")

@app.route("/support")
@login_required
@require_permission("support")
def support():
    return render_template("page.html", user=session["user"], title="Customer Support", desc="Guest Requests, WhatsApp, Complaints")

@app.route("/delivery")
@login_required
@require_permission("delivery")
def delivery():
    return render_template("page.html", user=session["user"], title="Delivery / Dispatch", desc="Delivery Notes, Tracking, Riders")

@app.route("/finance")
@login_required
@require_permission("finance")
def finance():
    return render_template("page.html", user=session["user"], title="Finance & Reports", desc="Income, Expenses, Reports, Reconcile")

@app.route("/users")
@login_required
@require_permission("users")
def users():
    return render_template("page.html", user=session["user"], title="Manage Users", desc="Owner Only: Add/Remove Staff, Approve Discounts")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)