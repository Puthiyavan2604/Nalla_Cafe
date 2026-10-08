class DiscountStrategy:
    def calculate(self, amount):
        raise NotImplementedError


class NoDiscountStrategy(DiscountStrategy):
    def calculate(self, amount):
        return 0


class StudentDiscountStrategy(DiscountStrategy):
    def calculate(self, amount):
        return amount * 0.10


class AddToCartCommand:
    def __init__(self, cart, product):
        self.cart = cart
        self.product = product
        self.added_item = None

    def execute(self):
        self.added_item = dict(self.product)
        self.cart.append(self.added_item)

    def undo(self):
        if self.added_item in self.cart:
            self.cart.remove(self.added_item)


class CommandInvoker:
    def __init__(self):
        self.history = []

    def execute(self, command):
        command.execute()
        self.history.append(command)

    def undo(self):
        command = self.history.pop()
        command.undo()

    def has_history(self):
        return bool(self.history)


class OrderSubject:
    def __init__(self):
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self, message):
        for observer in self.observers:
            observer.update(message)


class KitchenObserver:
    def update(self, message):
        print("KITCHEN:", message)


class CustomerObserver:
    def update(self, message):
        print("CUSTOMER:", message)


class OrderState:
    name = "UNKNOWN"

    def next_state(self):
        raise NotImplementedError


class PendingState(OrderState):
    name = "PENDING"

    def next_state(self):
        return PreparingState()


class PreparingState(OrderState):
    name = "PREPARING"

    def next_state(self):
        return ReadyState()


class ReadyState(OrderState):
    name = "READY"

    def next_state(self):
        return DeliveredState()


class DeliveredState(OrderState):
    name = "DELIVERED"

    def next_state(self):
        return self
