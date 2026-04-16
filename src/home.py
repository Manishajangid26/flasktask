from flask import flash, redirect, render_template, request, session, url_for

from src import app
from src.database import (
    create_order,
    get_order,
    get_product,
    list_products,
    save_contact,
    get_user_by_email,
    get_user_by_id,
    create_user,
    get_all_orders,
    update_order_status
)
from functools import wraps

@app.context_processor
def inject_user():
    user = None
    if "user_id" in session:
        user = get_user_by_id(session["user_id"])
    return dict(current_user=user)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in to access this page.", "warning")
            return redirect(url_for("login_page", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please log in as admin.", "error")
            return redirect(url_for("login_page"))
        user = get_user_by_id(session["user_id"])
        if not user or user.role != "admin":
            flash("You do not have permission to access that page.", "error")
            return redirect(url_for("homepage"))
        return f(*args, **kwargs)
    return decorated_function


def _cart_dict():
    if "cart" not in session or not isinstance(session["cart"], dict):
        session["cart"] = {}
    return session["cart"]


def _cart_lines():
    cart = _cart_dict()
    lines = []
    subtotal = 0.0
    for pid, qty in cart.items():
        try:
            q = int(qty)
            product_id = int(pid)
        except (TypeError, ValueError):
            continue
        if q <= 0:
            continue
        p = get_product(product_id)
        if not p:
            continue
        line_total = p["price"] * q
        subtotal += line_total
        lines.append(
            {
                "product": p,
                "quantity": q,
                "line_total": line_total,
            }
        )
    return lines, subtotal


@app.route("/")
def homepage():
    return render_template("home.html")


@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact_page():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip()
        message = (request.form.get("message") or "").strip()
        if not name or not email or not message:
            flash("Please fill in name, email, and message.", "error")
        else:
            save_contact(name, email, message)
            flash("Thank you! We will get back to you soon.", "success")
            return redirect(url_for("contact_page"))
    return render_template("contect.html")


@app.route("/products")
def products_page():
    raw = (request.args.get("category") or "").strip().lower()
    allowed = ("birthday", "wedding", "party", "eggless", "nonveg")
    category = raw if raw in allowed else None
    products = list_products(category=category)
    return render_template(
        "products.html",
        products=products,
        active_category=category,
    )


@app.route("/shops")
def shops_page():
    return render_template("shops.html")


@app.route("/cart", methods=["GET", "POST"])
def cart_page():
    cart = _cart_dict()
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add":
            pid = request.form.get("product_id")
            qty = request.form.get("quantity", "1")
            try:
                product_id = int(pid)
                q = max(1, int(qty))
            except (TypeError, ValueError):
                flash("Invalid product.", "error")
                return redirect(url_for("products_page"))
            if not get_product(product_id):
                flash("Product not found.", "error")
                return redirect(url_for("products_page"))
            key = str(product_id)
            cart[key] = int(cart.get(key, 0)) + q
            session.modified = True
            flash("Added to cart.", "success")
            return redirect(url_for("cart_page"))
        if action == "update":
            for key in list(cart.keys()):
                field = f"qty_{key}"
                if field in request.form:
                    try:
                        q = int(request.form.get(field, 0))
                    except ValueError:
                        q = 0
                    if q <= 0:
                        cart.pop(key, None)
                    else:
                        cart[key] = q
            session.modified = True
            flash("Cart updated.", "success")
            return redirect(url_for("cart_page"))
        if action == "remove":
            pid = request.form.get("product_id")
            if pid and str(pid) in cart:
                cart.pop(str(pid), None)
                session.modified = True
                flash("Item removed.", "success")
            return redirect(url_for("cart_page"))
    lines, subtotal = _cart_lines()
    return render_template("cart.html", lines=lines, subtotal=subtotal)


@app.route("/order", methods=["GET", "POST"])
def order_page():
    lines, subtotal = _cart_lines()
    if not lines:
        flash("Your cart is empty.", "error")
        return redirect(url_for("products_page"))
    if request.method == "POST":
        name = (request.form.get("customer_name") or "").strip()
        email = (request.form.get("email") or "").strip()
        phone = (request.form.get("phone") or "").strip()
        address = (request.form.get("address") or "").strip()
        if not name or not email or not phone or not address:
            flash("Please complete all delivery fields.", "error")
            return render_template(
                "order.html", lines=lines, subtotal=subtotal
            )
        session["checkout"] = {
            "customer_name": name,
            "email": email,
            "phone": phone,
            "address": address,
        }
        session.modified = True
        return redirect(url_for("payment_page"))
    return render_template("order.html", lines=lines, subtotal=subtotal)


@app.route("/payment", methods=["GET", "POST"])
def payment_page():
    lines, subtotal = _cart_lines()
    checkout = session.get("checkout")
    if not lines or not checkout:
        flash("Please start checkout from your cart.", "error")
        return redirect(url_for("cart_page"))
    if request.method == "POST":
        method = (request.form.get("payment_method") or "").strip()
        labels = {
            "cod": "Cash on delivery",
            "razorpay": "Paid via Razorpay",
            "upi_demo": "UPI (demo gateway)",
            "card_demo": "Card — Razorpay demo",
            "netbanking_demo": "Net banking (demo gateway)",
        }
        if method not in labels:
            flash("Choose a payment option.", "error")
            return render_template(
                "payment.html",
                lines=lines,
                subtotal=subtotal,
                checkout=checkout,
            )
        label = labels[method]
        if method == "razorpay":
            payment_id = request.form.get("razorpay_payment_id", "").strip()
            if payment_id:
                label += f" [ID: {payment_id}]"
                
        order_lines = []
        for line in lines:
            p = line["product"]
            order_lines.append(
                {
                    "product_id": p["id"],
                    "quantity": line["quantity"],
                    "unit_price": p["price"],
                }
            )
        order_id = create_order(
            checkout["customer_name"],
            checkout["email"],
            checkout["phone"],
            checkout["address"],
            subtotal,
            label,
            order_lines,
            user_id=session.get("user_id")
        )
        session.pop("cart", None)
        session.pop("checkout", None)
        session["last_order_id"] = order_id
        session.modified = True
        return redirect(url_for("confirmation_page", order_id=order_id))
    return render_template(
        "payment.html",
        lines=lines,
        subtotal=subtotal,
        checkout=checkout,
    )


@app.route("/confirmation/<int:order_id>")
def confirmation_page(order_id):
    order, items = get_order(order_id)
    if not order:
        flash("Order not found.", "error")
        return redirect(url_for("homepage"))
    return render_template("confirmation.html", order=order, items=items)


@app.route("/thank-you")
def thank_you_page():
    order_id = session.get("last_order_id")
    return render_template("thank_you.html", order_id=order_id)




@app.route('/menu')
def menu_page():
    occasion_filter = request.args.get('occasion', "").strip().lower()
    dietary_filter = request.args.get('dietary', "").strip().lower()
    
    allowed_occasions = ["birthday", "anniversary", "wedding", "party"]
    active_occasion = occasion_filter if occasion_filter in allowed_occasions else None
    
    from src.models import Product
    from src.extensions import db
    from src.database import _product_to_dict
    
    q = db.session.query(Product).order_by(Product.id)
    if active_occasion:
        q = q.filter(Product.occasion == active_occasion)
    
    if dietary_filter == 'eggless':
        q = q.filter(Product.description.ilike('%eggless%') | Product.name.ilike('%eggless%'))
    elif dietary_filter == 'with_egg':
        q = q.filter(~Product.description.ilike('%eggless%'), ~Product.name.ilike('%eggless%'))
        
    rows = q.all()
    # If no results and no occasion/dietary filters, just return all
    products = [_product_to_dict(p) for p in rows]
    
    return render_template(
        'menu.html', 
        products=products, 
        active_occasion=active_occasion
    )

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip()
        password = request.form.get("password")
        user = get_user_by_email(email)
        if user and user.check_password(password):
            session["user_id"] = user.id
            flash(f"Welcome back, {user.name}!", "success")
            return redirect(url_for("homepage"))
        flash("Invalid email or password.", "error")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip()
        password = request.form.get("password")
        if not name or not email or not password:
            flash("Please fill in all fields.", "error")
        else:
            user = create_user(name, email, password)
            if user:
                session["user_id"] = user.id
                flash("Registration successful!", "success")
                return redirect(url_for("homepage"))
            else:
                flash("Email already registered.", "error")
    return render_template("register.html")

@app.route("/logout")
def logout_page():
    session.pop("user_id", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("homepage"))


@app.route("/admin/orders")
@admin_required
def admin_orders_page():
    orders = get_all_orders()
    return render_template("admin_orders.html", orders=orders)


@app.route("/admin/orders/<int:order_id>/status", methods=["POST"])
@admin_required
def admin_update_order_status(order_id):
    new_status = request.form.get("status")
    if new_status and update_order_status(order_id, new_status):
        flash("Order status updated.", "success")
    else:
        flash("Invalid order or status.", "error")
    return redirect(url_for("admin_orders_page"))


@app.route("/track", methods=["GET", "POST"])
def track_order_page():
    order_data = None
    items = []
    
    order_id = request.args.get("order_id") or request.form.get("order_id")
    if order_id:
        try:
            oid = int(order_id)
            order_data, items = get_order(oid)
            
            if not order_data:
                flash("Order not found.", "error")
        except ValueError:
            flash("Invalid Order ID.", "error")
            
    return render_template("track_order.html", order=order_data, items=items)

