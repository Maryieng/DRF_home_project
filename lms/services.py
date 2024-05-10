import stripe
from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY


def create_product(product):
    """ Создание продукта """
    stripe_product = stripe.Product.create(name=product.title)
    return stripe_product.get("id")


def create_price(amount, product):
    """ Создание цены """
    stripe_price = stripe.Price.create(currency='rub', unit_amount=amount * 100, product_data={"name": "Payment"},
                                       product=product)
    return stripe_price.get("id")


def create_session(price):
    """ Сессия для ссылки на оплату """
    stripe_session = stripe.checkout.Session.create(success_url="http://127.0.0.1:8000",
                                                    line_items=[{"price": price, "quantity": 1}], mode="payment")
    return stripe_session.get("id"), stripe_session.get("url")
