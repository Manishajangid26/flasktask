from datetime import datetime

from sqlalchemy import inspect, text

from src.extensions import db
from src.models import ContactMessage, Order, OrderItem, Product


def _product_to_dict(p: Product):
    return {
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "image_url": p.image_url,
        "category": p.category,
        "occasion": getattr(p, "occasion", None),
    }


def _ensure_product_columns():
    inspector = inspect(db.engine)
    if "products" not in inspector.get_table_names():
        return
    cols = {c["name"] for c in inspector.get_columns("products")}
    with db.engine.begin() as conn:
        if "category" not in cols:
            conn.execute(text("ALTER TABLE products ADD COLUMN category VARCHAR(60)"))
        if "occasion" not in cols:
            conn.execute(text("ALTER TABLE products ADD COLUMN occasion VARCHAR(100)"))


def init_db():
    db.create_all()
    _ensure_product_columns()
    
    # Create default admin user if none exists
    from src.models import User
    if not db.session.query(User).filter_by(role='admin').first():
        admin = User(name='Admin', email='admin@freshbites.com', role='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()

    # Check if we specifically need to reset to the updated target items.
    if db.session.query(Product).count() != 185:
        db.session.query(OrderItem).delete()
        db.session.query(Order).delete()
        db.session.query(Product).delete()
        
        seed = [
            Product(
                name="Eggless Pineapple Cake [350 g]",
                description="Delicious Eggless Pineapple Cake [350 g]",
                price=229.0,
                image_url="./static/images/cake1.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Eggless Pineapple Cake [500 g]",
                description="Delicious Eggless Pineapple Cake [500 g]",
                price=379.0,
                image_url="https://images.unsplash.com/photo-1542826438-bd32f43d626f?w=600&q=80",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Strawberry Cake [350 g]",
                description="Delicious Strawberry Cake [350 g]",
                price=229.0,
                image_url="./static/images/cake4.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Strawberry Cake [500 g]",
                description="Delicious Strawberry Cake [500 g]",
                price=379.0,
                image_url="./static/images/cakeno4.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="White Forest Cake [350 g]",
                description="Delicious White Forest Cake [350 g]",
                price=229.0,
                image_url="https://images.unsplash.com/photo-1535141192574-5d4897c12636?w=600&q=80",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="White Forest Cake [500 g]",
                description="Delicious White Forest Cake [500 g]",
                price=379.0,
                image_url="./static/images/cake6.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Eggless Cassata Cake [350 g]",
                description="Delicious Eggless Cassata Cake [350 g]",
                price=229.0,
                image_url="./static/images/cake7.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Eggless Cassata Cake [500 g]",
                description="Delicious Eggless Cassata Cake [500 g]",
                price=379.0,
                image_url="./static/images/cake8.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Red Velvet Cake [350 g]",
                description="Delicious Red Velvet Cake [350 g]",
                price=239.0,
                image_url="./static/images/cake9.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Red Velvet Cake [500 g]",
                description="Delicious Red Velvet Cake [500 g]",
                price=389.0,
                image_url="./static/images/cake10.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Eggless Butterscotch Cake [350 g]",
                description="Delicious Eggless Butterscotch Cake [350 g]",
                price=279.0,
                image_url="./static/images/cake11.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Eggless Butterscotch Cake [500 g]",
                description="Delicious Eggless Butterscotch Cake [500 g]",
                price=389.0,
                image_url="./static/images/cake12.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Mixed Fruit Cake [350 g]",
                description="Delicious Mixed Fruit Cake [350 g]",
                price=289.0,
                image_url="./static/images/cake13.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Mixed Fruit Cake [500 g]",
                description="Delicious Mixed Fruit Cake [500 g]",
                price=399.0,
                image_url="./static/images/cake14.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Rasmalai Cake [350 g]",
                description="Delicious Rasmalai Cake [350 g]",
                price=249.0,
                image_url="./static/images/cake15.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Rasmalai Cake [500 g]",
                description="Delicious Rasmalai Cake [500 g]",
                price=399.0,
                image_url="./static/images/cake16.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="KitKat Cake [350 g]",
                description="Delicious KitKat Cake [350 g]",
                price=249.0,
                image_url="./static/images/cake17.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="KitKat Cake [500 g]",
                description="Delicious KitKat Cake [500 g]",
                price=399.0,
                image_url="./static/images/cake18.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Eggless Choco Vanilla Cake [350 g]",
                description="Delicious Eggless Choco Vanilla Cake [350 g]",
                price=269.0,
                image_url="./static/images/cake19.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Eggless Choco Vanilla Cake [500 g]",
                description="Delicious Eggless Choco Vanilla Cake [500 g]",
                price=409.0,
                image_url="./static/images/cake20.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Eggless Black Forest Cake [350 g]",
                description="Delicious Eggless Black Forest Cake [350 g]",
                price=279.0,
                image_url="./static/images/cake21.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Eggless Black Forest Cake [500 g]",
                description="Delicious Eggless Black Forest Cake [500 g]",
                price=409.0,
                image_url="./static/images/cake22.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Lite Chocolate Cake [350 g]",
                description="Delicious Lite Chocolate Cake [350 g]",
                price=279.0,
                image_url="./static/images/cake23.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Lite Chocolate Cake [500 g]",
                description="Delicious Lite Chocolate Cake [500 g]",
                price=429.0,
                image_url="./static/images/cake24.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Eggless Chocolate Cake [350 g]",
                description="Delicious Eggless Chocolate Cake [350 g]",
                price=279.0,
                image_url="https://images.unsplash.com/photo-1606890737304-57a1ca8a5b62?w=600&q=80",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Eggless Chocolate Cake [500 g]",
                description="Delicious Eggless Chocolate Cake [500 g]",
                price=429.0,
                image_url="./static/images/cake26.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Choco Fudge Cake [350 g]",
                description="Delicious Choco Fudge Cake [350 g]",
                price=299.0,
                image_url="./static/images/cake27.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Choco Fudge Cake [500 g]",
                description="Delicious Choco Fudge Cake [500 g]",
                price=429.0,
                image_url="./static/images/cake28.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Dark forest cake",
                description="Delicious Dark forest cake",
                price=300.0,
                image_url="./static/images/cake29.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Chocolate Truffle Cake",
                description="Delicious Chocolate Truffle Cake",
                price=350.0,
                image_url="./static/images/cake30.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Choco Chips Cake",
                description="Delicious Choco Chips Cake",
                price=300.0,
                image_url="./static/images/cake31.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Chocolate Oreo Cake [350 g]",
                description="Delicious Chocolate Oreo Cake [350 g]",
                price=350.0,
                image_url="./static/images/cake32.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Macha Chocolate cake",
                description="Delicious Macha Chocolate cake",
                price=300.0,
                image_url="./static/images/cake33.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Punch Chocolate cake",
                description="Delicious Punch Chocolate cake",
                price=300.0,
                image_url="https://images.unsplash.com/photo-1588195538326-c5b1e9f80a1b?w=600&q=80",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Chocolate Truffle Cake [500 g]",
                description="Delicious Chocolate Truffle Cake [500 g]",
                price=549.0,
                image_url="./static/images/cake35.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Father's day special cake",
                description="Delicious Father's day special cake",
                price=350.0,
                image_url="./static/images/cake36.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Mother's day special cake",
                description="Delicious Mother's day special cake",
                price=350.0,
                image_url="./static/images/cake37.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="New year special cake",
                description="Delicious New year special cake",
                price=350.0,
                image_url="./static/images/cake38.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Friendship Day Special Cake",
                description="Delicious Friendship Day Special Cake",
                price=350.0,
                image_url="./static/images/cake39.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Eggless Kanha Cake [500 g]",
                description="Delicious Eggless Kanha Cake [500 g]",
                price=500.0,
                image_url="./static/images/cake40.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Krishna matki cake",
                description="Delicious Krishna matki cake",
                price=550.0,
                image_url="./static/images/cake41.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Janmashtami cake special eggless cake",
                description="Delicious Janmashtami cake special eggless cake",
                price=550.0,
                image_url="./static/images/cake42.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Mother Day Cake [400 g]",
                description="Delicious Mother Day Cake [400 g]",
                price=350.0,
                image_url="./static/images/cake43.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Eggless Chocolate Cake [400 g]",
                description="Delicious Eggless Chocolate Cake [400 g]",
                price=400.0,
                image_url="./static/images/cake44.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Mother Day Special [400 g]",
                description="Delicious Mother Day Special [400 g]",
                price=400.0,
                image_url="./static/images/cake45.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Shree Krishna janmashtami specal cake",
                description="Delicious Shree Krishna janmashtami specal cake",
                price=400.0,
                image_url="./static/images/cake46.png",
                category="Cakes",
                occasion="general"
            ),
            Product(
                name="Pineapple Pudding",
                description="Delicious Pineapple Pudding",
                price=99.0,
                image_url="./static/images/cake47.png",
                category="Puddings",
                occasion="general"
            ),
            Product(
                name="Butterscotch Pudding",
                description="Delicious Butterscotch Pudding",
                price=99.0,
                image_url="./static/images/cake48.png",
                category="Puddings",
                occasion="general"
            ),
            Product(
                name="Strawberry Pudding",
                description="Delicious Strawberry Pudding",
                price=99.0,
                image_url="./static/images/cake49.png",
                category="Puddings",
                occasion="general"
            ),
            Product(
                name="Chocolate Pudding",
                description="Delicious Chocolate Pudding",
                price=99.0,
                image_url="./static/images/cake50.png",
                category="Puddings",
                occasion="general"
            ),
            Product(
                name="Chocolate Pastry",
                description="Delicious Chocolate Pastry",
                price=129.0,
                image_url="./static/images/cake51.png",
                category="Pastries",
                occasion="general"
            ),
            Product(
                name="Chocolate Truffle with Brownie Pastry",
                description="Delicious Chocolate Truffle with Brownie Pastry",
                price=170.0,
                image_url="./static/images/cake52.png",
                category="Pastries",
                occasion="general"
            ),
            Product(
                name="Choco Chip Pastry",
                description="Delicious Choco Chip Pastry",
                price=150.0,
                image_url="./static/images/cake53.png",
                category="Pastries",
                occasion="general"
            ),
            Product(
                name="Black Forest Pastry",
                description="Delicious Black Forest Pastry",
                price=129.0,
                image_url="./static/images/cake54.png",
                category="Pastries",
                occasion="general"
            ),
            Product(
                name="Chocolate Cream Rolls",
                description="Delicious Chocolate Cream Rolls",
                price=99.0,
                image_url="./static/images/cake55.png",
                category="Cream roll",
                occasion="general"
            ),
            Product(
                name="Vanilla Rolls",
                description="Delicious Vanilla Rolls",
                price=69.0,
                image_url="./static/images/cake56.png",
                category="Cream roll",
                occasion="general"
            ),
            Product(
                name="Jem Rolls",
                description="Delicious Jem Rolls",
                price=150.0,
                image_url="./static/images/cake57.png",
                category="Cream roll",
                occasion="general"
            ),
            Product(
                name="Hot Chocolate",
                description="Delicious Hot Chocolate",
                price=149.0,
                image_url="./static/images/cake58.png",
                category="Desserts",
                occasion="general"
            ),
            Product(
                name="Brownie With Ice Cream",
                description="Delicious Brownie With Ice Cream",
                price=189.0,
                image_url="./static/images/cake59.png",
                category="Desserts",
                occasion="general"
            ),
            Product(
                name="Rich Pineapple Bento Cake [200 g]",
                description="Delicious Rich Pineapple Bento Cake [200 g]",
                price=300.0,
                image_url="./static/images/cake60.png",
                category="Fathers Day Special",
                occasion="general"
            ),
            Product(
                name="Fathers Day Vanilla Bento Cake [200 g]",
                description="Delicious Fathers Day Vanilla Bento Cake [200 g]",
                price=300.0,
                image_url="./static/images/cake61.png",
                category="Fathers Day Special",
                occasion="general"
            ),
            Product(
                name="Father Day Special Chocolate Cake [350 g]",
                description="Delicious Father Day Special Chocolate Cake [350 g]",
                price=350.0,
                image_url="./static/images/cake62.png",
                category="Fathers Day Special",
                occasion="general"
            ),
            Product(
                name="Happy Father's Day Cake",
                description="Delicious Happy Father's Day Cake",
                price=350.0,
                image_url="./static/images/cake63.png",
                category="Fathers Day Special",
                occasion="general"
            ),
            Product(
                name="Fathers Day Pineapple Cake [350 g]",
                description="Delicious Fathers Day Pineapple Cake [350 g]",
                price=400.0,
                image_url="./static/images/cake64.png",
                category="Fathers Day Special",
                occasion="general"
            ),
            Product(
                name="Father's Day Special I Love Papa Cake",
                description="Delicious Father's Day Special I Love Papa Cake",
                price=400.0,
                image_url="./static/images/cake65.png",
                category="Fathers Day Special",
                occasion="general"
            )
        ]
        
        occasions_to_add = ['birthday', 'anniversary', 'wedding', 'party']
        birthday_images = [
            "bithday1.png", "birthday2.png", "birthday3.png", "birthday4.png", "birthday5.png",
            "birthday.png", "birthday7.png", "birthday8.png", "birthday.png", "birthday10.png",
            "birthday11.png", "birthday12.png", "birthday13.png", "birthday14.png", "birthday15.png",
            "birthday16.png", "birthday17.png", "birthday18.png", "bithday19.png", "bithday20.png",
            "birthday21.png", "birthday22.png", "birthday23.png", "birthday24.png", "birthday25.png",
            "birthday26.png", "birthday27.png", "birthday28.png", "birthday29.png", "birthday30.png"
        ]
        anniversary_images = [f"ani{i+1}.png" for i in range(30)]
        wedding_images = [f"wed{i+1}.png" for i in range(30)]
        party_images = [f"par{i+1}.png" for i in range(30)]

        for occ in occasions_to_add:
            for i in range(30):
                orig = seed[i]
                
                img_url = orig.image_url
                if occ == 'birthday':
                    img_url = f"./static/images/{birthday_images[i]}"
                elif occ == 'anniversary':
                    img_url = f"./static/images/{anniversary_images[i]}"
                elif occ == 'wedding':
                    img_url = f"./static/images/{wedding_images[i]}"
                elif occ == 'party':
                    img_url = f"./static/images/{party_images[i]}"
                    
                new_price = orig.price
                if '500 g' in orig.name:
                    new_price += 100
                elif '400 g' in orig.name:
                    new_price += 75
                elif '350 g' in orig.name:
                    new_price += 50
                elif '200 g' in orig.name:
                    new_price += 30
                else:
                    new_price += 50
                    
                seed.append(Product(
                    name=f"{occ.capitalize()} Special {orig.name}",
                    description=f"{occ.capitalize()} Special - {orig.description}",
                    price=new_price,
                    image_url=img_url,
                    category=orig.category,
                    occasion=occ
                ))

        db.session.add_all(seed)
        db.session.commit()


def list_products(category=None):
    q = db.session.query(Product).order_by(Product.id)
    if category:
        q = q.filter(Product.category == category)
    rows = q.all()
    return [_product_to_dict(p) for p in rows]


def get_product(product_id):
    p = db.session.get(Product, product_id)
    return _product_to_dict(p) if p else None


def save_contact(name, email, message):
    msg = ContactMessage(
        name=name,
        email=email,
        message=message,
        created_at=datetime.utcnow(),
    )
    db.session.add(msg)
    db.session.commit()


def create_order(customer_name, email, phone, address, total, payment_method, lines, user_id=None):
    """
    lines: list of dicts with keys product_id, quantity, unit_price
    """
    order = Order(
        customer_name=customer_name,
        email=email,
        phone=phone,
        address=address,
        total=total,
        payment_method=payment_method,
        status="confirmed",
        user_id=user_id,
        created_at=datetime.utcnow(),
    )
    db.session.add(order)
    db.session.flush()
    for line in lines:
        db.session.add(
            OrderItem(
                order_id=order.id,
                product_id=line["product_id"],
                quantity=line["quantity"],
                unit_price=line["unit_price"],
            )
        )
    db.session.commit()
    return order.id


def get_order(order_id):
    o = db.session.get(Order, order_id)
    if not o:
        return None, []
    order_dict = {
        "id": o.id,
        "customer_name": o.customer_name,
        "email": o.email,
        "phone": o.phone,
        "address": o.address,
        "total": o.total,
        "payment_method": o.payment_method,
        "status": o.status,
        "created_at": o.created_at.isoformat() if o.created_at else "",
    }
    items = []
    for oi in o.items:
        items.append(
            {
                "product_id": oi.product_id,
                "quantity": oi.quantity,
                "unit_price": oi.unit_price,
                "name": oi.product.name if oi.product else "",
            }
        )
    return order_dict, items


def get_all_orders():
    orders = db.session.query(Order).order_by(Order.created_at.desc()).all()
    result = []
    for o in orders:
        result.append({
            "id": o.id,
            "customer_name": o.customer_name,
            "email": o.email,
            "phone": o.phone,
            "address": o.address,
            "total": o.total,
            "payment_method": o.payment_method,
            "status": o.status,
            "created_at": o.created_at.isoformat() if o.created_at else "",
        })
    return result


def update_order_status(order_id, status):
    o = db.session.get(Order, order_id)
    if o:
        o.status = status
        db.session.commit()
        return True
    return False


def get_user_by_email(email):
    from src.models import User
    return db.session.query(User).filter_by(email=email).first()


def get_user_by_id(user_id):
    from src.models import User
    return db.session.get(User, user_id)


def create_user(name, email, password, role="user"):
    from src.models import User
    if get_user_by_email(email):
        return None
    user = User(name=name, email=email, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user
