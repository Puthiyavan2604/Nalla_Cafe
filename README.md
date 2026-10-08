# Campus Cafe - Flask Design Pattern Project

A small café ordering website made using Python Flask, HTML, CSS and JavaScript.

The application uses MVC as the main application architecture and demonstrates 10 design patterns in the backend.

## Design patterns used

### Creational
1. Singleton - AppConfig
2. Factory Method - ProductFactory
3. Builder - OrderBuilder

### Structural
4. Adapter - LegacyPaymentAdapter
5. Decorator - CheeseDecorator
6. Facade - CafeFacade

### Behavioral
7. Command - AddToCartCommand and CommandInvoker
8. Observer - OrderSubject, KitchenObserver, CustomerObserver
9. State - PendingState, PreparingState, ReadyState, DeliveredState
10. Strategy - StudentDiscountStrategy and NoDiscountStrategy

## MVC structure

Model:
- Product data
- Cart data
- Order data
- Design pattern classes

View:
- templates/index.html
- static/style.css

Controller:
- app.py Flask routes

## Run

### Windows

```text
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open:

http://127.0.0.1:5000

### Linux/macOS

```text
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open:

http://127.0.0.1:5000

## How to demonstrate

1. Add a food item to the cart.
2. Add another item and use Undo.
3. Select Student discount.
4. Select Add cheese to food.
5. Place the order.
6. Check the Flask terminal for kitchen and customer notifications.
7. Use Move to Next State to change the order from PENDING to PREPARING, READY and DELIVERED.

The frontend is kept simple because the main purpose of the project is to demonstrate the backend design patterns and MVC architecture.
