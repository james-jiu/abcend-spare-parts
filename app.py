from flask import Flask, render_template_string, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = "abcend-secret"

# REAL PRODUCTS - Stock and Dashboard go use same list
PRODUCTS = [
    {"id": 1, "name": "Volvo Brake Pad", "brand": "Volvo", "price": 45000, "qty": 12},
    {"id": 2, "name": "Mack Clutch Kit", "brand": "Mack", "price": 120000, "qty": 5},
    {"id": 3, "name": "Toyota Oil Filter", "brand": "Toyota", "price": 15000, "qty": 30},
    {"id": 4, "name": "Iveco Air Filter", "brand": "Iveco", "price": 25000, "qty": 18},
    {"id": 5, "name": "Mercedes Fuel Pump", "brand": "Mercedes", "price": 85000, "qty": 7},
]

MENU = """
<div style="background:#1a1a2e;color:white;padding:15px;display:flex;gap:20px">
<a href="/dashboard" style="color:white;text-decoration:none">Dashboard</a>
<a href="/stock" style="color:white;text-decoration:none">Stock</a>
<a href="/logout" style="color:white;text-decoration:none">Logout</a>
</div>
"""

@app.route("/")
def home():
    return redirect("/login")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form.get("username")=="jameel" and request.form.get("password")=="admin123":
            session["user"]="Jameel"
            return redirect("/dashboard")
        return "Wrong login, <a href='/login'>try again</a>"
    return """
    <h2 style="text-align:center">ABCEND SPARE PARTS</h2>
    <form method="post" style="max-width:300px;margin:auto">
    Username:<br><input name="username" style="width:100%;padding:10px"><br><br>
    Password:<br><input name="password" type="password" style="width:100%;padding:10px"><br><br>
    <button style="width:100%;padding:12px;background:#1a1a2e;color:white">LOGIN</button>
    </form>
    """

@app.route("/dashboard")
def dashboard():
    if "user" not in session: return redirect("/login")
    total = sum(p["price"]*p["qty"] for p in PRODUCTS)
    rows = "".join([f"<tr><td>{p['name']}</td><td>{p['brand']}</td><td>₦{p['price']:,}</td><td>{p['qty']}</td></tr>" for p in PRODUCTS])
    return MENU + f"""
    <h2>Welcome, Jameel!</h2>
    <p><b>Total Stock Value:</b> ₦{total:,} | <b>Products:</b> {len(PRODUCTS)}</p>
    <table border="1" cellpadding="10" style="width:100%">{rows}</table>
    """

@app.route("/stock")
def stock():
    if "user" not in session: return redirect("/login")
    rows = "".join([f"<tr><td>{p['name']}</td><td>{p['brand']}</td><td>₦{p['price']:,}</td><td>{p['qty']}</td><td><a href='/delete/{p['id']}'>Delete</a></td></tr>" for p in PRODUCTS])
    return MENU + f"""
    <h2>Stock Management</h2>
    <a href="/add-stock"><button style="padding:10px;background:green;color:white">+ Add Stock</button></a><br><br>
    <table border="1" cellpadding="10" style="width:100%">{rows}</table>
    """

@app.route("/add-stock", methods=["GET","POST"])
def add_stock():
    if "user" not in session: return redirect("/login")
    if request.method=="POST":
        new_id = max([p["id"] for p in PRODUCTS], default=0)+1
        PRODUCTS.append({
            "id": new_id,
            "name": request.form.get("name"),
            "brand": request.form.get("brand"),
            "price": int(request.form.get("price") or 0),
            "qty": int(request.form.get("qty") or 0),
        })
        return redirect("/stock")
    return MENU + """
    <h2>Add New Product</h2>
    <form method="post" style="max-width:300px">
    Name:<br><input name="name" required style="width:100%;padding:10px"><br><br>
    Brand:<br><input name="brand" required style="width:100%;padding:10px"><br><br>
    Price:<br><input name="price" type="number" required style="width:100%;padding:10px"><br><br>
    Quantity:<br><input name="qty" type="number" required style="width:100%;padding:10px"><br><br>
    <button style="padding:12px;background:green;color:white">SAVE PRODUCT</button>
    </form>
    """

@app.route("/delete/<int:pid>")
def delete(pid):
    global PRODUCTS
    PRODUCTS = [p for p in PRODUCTS if p["id"]!=pid]
    return redirect("/stock")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))
