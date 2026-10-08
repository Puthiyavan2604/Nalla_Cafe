from copy import deepcopy


class AppConfig:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.host = "127.0.0.1"
            cls._instance.port = 5000
        return cls._instance


class ProductFactory:
    def create_products(self):
        return [
            {"id": 1, "name": "Veg Burger", "category": "Food", "price": 90},
            {"id": 2, "name": "Paneer Wrap", "category": "Food", "price": 110},
            {"id": 3, "name": "Cold Coffee", "category": "Drink", "price": 70},
            {"id": 4, "name": "Lemon Soda", "category": "Drink", "price": 50}
        ]


class OrderBuilder:
    _next_id = 1001

    def __init__(self):
        self.order = {
            "id": None,
            "customer": "Student",
            "items": [],
            "subtotal": 0,
            "discount": 0,
            "total": 0
        }

    def set_customer(self, customer):
        self.order["customer"] = customer
        return self

    def set_items(self, items):
        self.order["items"] = deepcopy(items)
        return self

    def set_subtotal(self, subtotal):
        self.order["subtotal"] = subtotal
        return self

    def set_discount(self, discount):
        self.order["discount"] = discount
        return self

    def set_total(self, total):
        self.order["total"] = total
        return self

    def build(self):
        self.order["id"] = OrderBuilder._next_id
        OrderBuilder._next_id += 1
        return self.order
