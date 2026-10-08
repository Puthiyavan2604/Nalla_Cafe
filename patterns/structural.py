class LegacyPaymentSystem:
    def make_payment_in_rupees(self, amount):
        return {
            "success": True,
            "message": f"Payment of ₹{amount:.2f} completed"
        }


class LegacyPaymentAdapter:
    def __init__(self):
        self.legacy = LegacyPaymentSystem()

    def pay(self, amount):
        return self.legacy.make_payment_in_rupees(amount)


class CheeseDecorator:
    def __init__(self, product):
        self.product = product

    def to_dict(self):
        item = dict(self.product)
        item["name"] = item["name"] + " + Cheese"
        item["price"] += 20
        return item


class CafeFacade:
    def __init__(self, payment_service):
        self.payment_service = payment_service

    def checkout(self, amount):
        if amount <= 0:
            return {"success": False, "message": "Invalid amount"}

        return self.payment_service.pay(amount)
