import os

from flask import Flask, session

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(os.path.dirname(basedir), "bakery.db")

app = Flask(
    __name__,
    template_folder=os.path.join(basedir, "templates"),
    static_folder=os.path.join(basedir, "..", "static"),
)
app.secret_key = os.environ.get("SECRET_KEY", "dev-bakery-secret-change-in-production")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", f"sqlite:///{instance_path}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

from src.extensions import db

db.init_app(app)

import src.models  # noqa: F401, E402 — register models before create_all

from src.database import get_product, init_db

with app.app_context():
    init_db()


@app.context_processor
def inject_navbar_catalog():
    from src.models import Product

    products = Product.query.order_by(Product.id).all()
    by_cat = {}
    for p in products:
        key = (p.category or "other").lower()
        by_cat.setdefault(key, []).append(p)
    return {"cakes_by_cat": by_cat, "nav_products": products}


@app.context_processor
def inject_cart_state():
    cart = session.get("cart") or {}
    count = sum(int(q) for q in cart.values() if str(q).isdigit())
    preview = []
    subtotal = 0.0
    for pid, qty in cart.items():
        if not str(qty).isdigit():
            continue
        q = int(qty)
        if q <= 0:
            continue
        try:
            product_id = int(pid)
        except (TypeError, ValueError):
            continue
        p = get_product(product_id)
        if not p:
            continue
        line_total = p["price"] * q
        subtotal += line_total
        preview.append({"product": p, "quantity": q, "line_total": line_total})
    return {
        "cart_item_count": count,
        "cart_preview_lines": preview[:5],
        "cart_preview_subtotal": subtotal,
    }


from src import home  # noqa: E402, F401
