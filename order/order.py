from decimal import Decimal

from django.conf import settings

from product.models import ProductModel


from .models import OrderModel


class Order():
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get(settings.ORDER_SESSION_ID)
        header = self.session.get
        if not cart:
            cart = self.session[settings.ORDER_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0, "price": str(product.price)}
        if update_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.save()

    def save(self):
        self.session[settings.ORDER_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        if str(product.id) in self.cart:
            del self.cart[str(product.id)]
            self.save()

    def get_products(self):
        product_ids = self.cart.keys()
        products = ProductModel.objects.filter(id__in=product_ids)
        return products

    def __iter__(self):
        product_ids = self.cart.keys()
        products = ProductModel.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]["product"] = product

        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.ORDER_SESSION_ID]
        self.session.modified = True

    def create_order(self, sub=False):

        if not sub:

            o = OrderModel.objects.create(
                user=self.request.user,
                price=self.get_total_price(),
                payment=False,
                order_type="1",
                status="0"
            )
            o.products.set(self.get_products())
            o.save()
            return o
