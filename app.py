from flask import Flask, render_template, request, jsonify

from patterns.creational import AppConfig, ProductFactory, OrderBuilder
from patterns.structural import LegacyPaymentAdapter, CheeseDecorator, CafeFacade
from patterns.behavioral import (
    StudentDiscountStrategy, NoDiscountStrategy,
    AddToCartCommand, CommandInvoker,
    OrderSubject, KitchenObserver, CustomerObserver,
    PendingState, PreparingState, ReadyState, DeliveredState
)

app = Flask(__name__)

config = AppConfig()
factory = ProductFactory()
payment = LegacyPaymentAdapter()
facade = CafeFacade(payment)

products = factory.create_products()

cart = []
invoker = CommandInvoker()

order_subject = OrderSubject()
order_subject.attach(KitchenObserver())
order_subject.attach(CustomerObserver())

order_state = PendingState()
last_order = None


@app.route("/")
def home():
    return render_template("index.html", products=products)


@app.route("/api/cart", methods=["GET"])
def get_cart():
    total = sum(item["price"] for item in cart)
    return jsonify({"items": cart, "total": total})


@app.route("/api/cart/add", methods=["POST"])
def add_to_cart():
    data = request.get_json()
    product_id = int(data["product_id"])

    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    command = AddToCartCommand(cart, product)
    invoker.execute(command)

    return get_cart()


@app.route("/api/cart/undo", methods=["POST"])
def undo_cart():
    if not invoker.has_history():
        return jsonify({"error": "Nothing to undo"}), 400

    invoker.undo()
    return get_cart()


@app.route("/api/checkout", methods=["POST"])
def checkout():
    global last_order, order_state

    if not cart:
        return jsonify({"error": "Cart is empty"}), 400

    data = request.get_json() or {}
    student = data.get("student", False)
    cheese = data.get("cheese", False)

    items = [dict(item) for item in cart]

    if cheese:
        items = [
            CheeseDecorator(item).to_dict()
            if item["category"] == "Food"
            else item
            for item in items
        ]

    subtotal = sum(item["price"] for item in items)

    strategy = (
        StudentDiscountStrategy()
        if student
        else NoDiscountStrategy()
    )

    discount = strategy.calculate(subtotal)
    final_total = subtotal - discount

    order = (
        OrderBuilder()
        .set_customer(data.get("customer", "Student"))
        .set_items(items)
        .set_subtotal(subtotal)
        .set_discount(discount)
        .set_total(final_total)
        .build()
    )

    payment_result = facade.checkout(final_total)

    if not payment_result["success"]:
        return jsonify({"error": payment_result["message"]}), 400

    last_order = order
    order_state = PendingState()
    order_subject.notify(f"Order #{order['id']} placed")

    cart.clear()

    return jsonify({
        "success": True,
        "order": order,
        "payment": payment_result,
        "state": order_state.name
    })


@app.route("/api/order/state", methods=["GET"])
def get_order_state():
    return jsonify({
        "state": order_state.name if last_order else "NO ORDER"
    })


@app.route("/api/order/next", methods=["POST"])
def next_order_state():
    global order_state

    if not last_order:
        return jsonify({"error": "Place an order first"}), 400

    order_state = order_state.next_state()

    return jsonify({"state": order_state.name})


if __name__ == "__main__":
    app.run(host=config.host, port=config.port, debug=True)
