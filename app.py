from flask import Flask, render_template, request, redirect, Response
from database import Session, engine, Base
from models import Customer, Bag, Order
import os

app = Flask(__name__)

# CREATE TABLES
Base.metadata.create_all(engine)


# ===============================
# STEP 2: INSERT 22 BAGS (RUN ONCE)
# ===============================
def seed_data():
    db = Session()
    try:
        if db.query(Bag).count() == 0:

            def load_image(filename):
                path = os.path.join("static/images", filename)
                with open(path, "rb") as f:
                    return f.read()

            bags = [
                Bag(name="Backpack", category="Everyday", description="School/work backpack", price=1200, image=load_image("backpack.jpg")),
                Bag(name="Messenger Bag", category="Everyday", description="Crossbody office bag", price=1500, image=load_image("messenger_bag.jpg")),
                Bag(name="Briefcase", category="Work", description="Formal business bag", price=2500, image=load_image("briefcase.jpg")),
                Bag(name="Laptop Bag", category="Work", description="Laptop carrier", price=1800, image=load_image("laptop_bag.jpg")),
                Bag(name="Satchel", category="Casual", description="Classic satchel bag", price=1600, image=load_image("satchel.jpg")),
                Bag(name="Portfolio Bag", category="Work", description="Slim document holder", price=1400, image=load_image("portfolio_bag.jpg")),

                Bag(name="Duffel Bag", category="Travel", description="Large travel bag", price=2000, image=load_image("duffel_bag.jpg")),
                Bag(name="Weekender Bag", category="Travel", description="Short trip bag", price=2200, image=load_image("weekender_bag.jpg")),
                Bag(name="Gym Bag", category="Sports", description="Workout bag", price=1300, image=load_image("gym_bag.jpg")),
                Bag(name="Travel Bag", category="Travel", description="General travel bag", price=2100, image=load_image("travel_bag.jpg")),
                Bag(name="Carry-On Bag", category="Travel", description="Airline cabin bag", price=3000, image=load_image("carry-on_bag.jpg")),
                Bag(name="Garment Bag", category="Travel", description="Suit storage bag", price=1900, image=load_image("garment_bag.jpg")),

                Bag(name="Crossbody Bag", category="Casual", description="Compact crossbody", price=900, image=load_image("crossbody_bag.jpg")),
                Bag(name="Sling Bag", category="Casual", description="One-strap bag", price=800, image=load_image("sling_bag.jpg")),
                Bag(name="Tote Bag", category="Casual", description="Open shopping bag", price=1000, image=load_image("tote_bag.jpg")),
                Bag(name="Waist Bag", category="Casual", description="Fanny pack", price=700, image=load_image("waist_bag.jpg")),
                Bag(name="Shoulder Bag", category="Casual", description="Single strap bag", price=1100, image=load_image("shoulder_bag.jpg")),
                Bag(name="Clutch", category="Casual", description="Small pouch bag", price=600, image=load_image("clutch.jpg")),

                Bag(name="Camera Bag", category="Special", description="Camera storage", price=1700, image=load_image("camera_bag.jpg")),
                Bag(name="Dopp Kit", category="Special", description="Toiletry bag", price=900, image=load_image("dopp-kit_bag.jpg")),
                Bag(name="Tool Bag", category="Special", description="Tool storage bag", price=1500, image=load_image("tool_bag.jpg")),
                Bag(name="Hydration Pack", category="Special", description="Water backpack", price=1600, image=load_image("hydration_pack.jpg")),
            ]

            db.add_all(bags)
            db.commit()
    finally:
        db.close()


seed_data()


# ===============================
# ROUTES
# ===============================

@app.route('/')
def home():
    db = Session()
    try:
        bags = db.query(Bag).all()
        orders = db.query(Order).all()
        return render_template('index.html', bags=bags, orders=orders)
    finally:
        db.close()


@app.route('/add_order', methods=['POST'])
def add_order():
    db = Session()
    try:
        name = request.form['name']
        contact = request.form['contact']
        bag_id = request.form['bag_id']

        customer = Customer(name=name, contact=contact)
        db.add(customer)
        db.commit()

        order = Order(customer_id=customer.id, bag_id=bag_id)
        db.add(order)
        db.commit()

        return redirect('/')
    finally:
        db.close()


# ===============================
# IMAGE ROUTE
# ===============================
@app.route('/image/<int:bag_id>')
def get_image(bag_id):
    db = Session()
    try:
        bag = db.get(Bag, bag_id)

        if not bag or not bag.image:
            return "No image", 404

        return Response(bag.image, mimetype='image/jpeg')

    except Exception as e:
        print("ERROR:", e)
        return "Error loading image", 500

    finally:
        db.close()


# ===============================
# RUN APP
# ===============================
if __name__ == '__main__':
    app.run(debug=True)
