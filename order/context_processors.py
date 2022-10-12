from .order import Order


def OrderInfos(requset):
    order = Order(requset)
    order.clear()
    return {
        "order": order
    }
