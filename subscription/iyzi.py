import iyzipay
from iyzipay.iyzipay_resource import IyzipayResource

options = {
    'api_key': ' ',
    'secret_key': ' ',
    'base_url': iyzipay.base_url
}


class Product(IyzipayResource):
    def create(self, request, foptions):
        return self.connect('POST', '/v2/subscription/products', foptions, request)

    def update(self, request, foptions):
        if request.get('productReferenceCode') is None:
            raise Exception('token must be in request')
        token = str(request.get('productReferenceCode'))
        return self.connect('POST', '/v2/subscription/products/'+token, foptions, request)

    def delete(self, request, foptions):
        if request.get('productReferenceCode') is None:
            raise Exception('token must be in request')
        token = request.get('productReferenceCode')
        return self.connect('DELETE', '/v2/subscription/products/'+token, foptions, request)

    def detail(self, request, foptions):
        if request.get('productReferenceCode') is None:
            raise Exception('token must be in request')
        token = request.get('productReferenceCode')
        return self.connect('GET', '/v2/subscription/products/'+token, foptions, request)

    def get(self, request, foptions):
        page = str(request.get('page') or 1)
        count = str(request.get('count') or 10)
        return self.connect('GET', '/v2/subscription/products/?page='+page+'&count='+count, foptions)


class Plan(IyzipayResource):
    def create(self, request, foptions):
        if request.get('productReferenceCode') is None:
            raise Exception('token must be in request')
        token = str(request.get('productReferenceCode'))
        return self.connect('POST', '/v2/subscription/products/'+token+'/pricing-plans', foptions, request)

    def update(self, request, foptions):
        if request.get('pricingPlanReferenceCode') is None:
            raise Exception('pricingPlanReferenceCode must be in request')
        token = str(request.get('pricingPlanReferenceCode'))
        return self. connect('POST', '/v2/subscription/pricing-plans/'+token, foptions, request)

    def delete(self, request, foptions):
        if request.get('pricingPlanReferenceCode') is None:
            raise Exception('pricingPlanReferenceCode must be in request')
        token = str(request.get('pricingPlanReferenceCode'))
        return self. connect('DELETE', '/v2/subscription/pricing-plans/'+token, foptions, request)

    def detail(self, request, foptions):
        if request.get('pricingPlanReferenceCode') is None:
            raise Exception('pricingPlanReferenceCode must be in request')
        token = str(request.get('pricingPlanReferenceCode'))
        return self. connect('GET', '/v2/subscription/pricing-plans/'+token, foptions)

    def get(self, request, foptions):
        page = str(request.get('page') or 1)
        count = str(request.get('count') or 10)
        if request.get('productReferenceCode') is None:
            raise Exception('productReferenceCode must be in request')
        token = str(request.get('productReferenceCode'))
        return self. connect('GET', '/v2/subscription/products/' + token + '/pricing-plans/', foptions, request)


class Customer(IyzipayResource):
    def create(self, request, foptions):
        return self.connect('POST', '/v2/subscription/customers', foptions, request)

    def update(self, request, foptions):
        if request.get('customerReferenceCode') is None:
            raise Exception('customerReferenceCode must be in request')
        token = str(request.get('customerReferenceCode'))
        return self.connect('POST', '/v2/subscription/customers/'+token, foptions, request)

    def detail(self, request, foptions):
        if request.get('customerReferenceCode') is None:
            raise Exception('customerReferenceCode must be in request')
        token = str(request.get('customerReferenceCode'))
        return self.connect('GET', '/v2/subscription/customers/'+token, foptions)

    def get(self, request, foptions):
        page = str(request.get('page') or 1)
        count = str(request.get('count') or 10)
        return self.connect('GET', '/v2/subscription/customers/', foptions, request)


class Subscription(IyzipayResource):
    def checkout(self, request, foptions):
        return self.connect('POST', '/v2/subscription/checkoutform/initialize', foptions, request)

    def api(self, request, foptions):
        return self.connect('POST', '/v2/subscription/initialize', foptions, request)

    def activate(self, request, foptions):
        if request.get('subscriptionReferenceCode') is None:
            raise Exception('subscriptionReferenceCode must be in request')
        token = request.get('subscriptionReferenceCode')
        return self.connect('POST', '/v2/subscription/subscriptions/' + token + '/activate', foptions, request)

    def retry(self, request, foptions):
        if request.get('referenceCode') is None:
            raise Exception('referenceCode must be in request')
        return self.connect('POST', '/v2/subscription/operation/retry', foptions, request)

    def upgrade(self, request, foptions):
        if request.get('subscriptionReferenceCode') is None:
            raise Exception('subscriptionReferenceCode must be in request')
        token = request.get('subscriptionReferenceCode')
        return self.connect('POST', '/v2/subscription/subscriptions/' + token + '/upgrade', foptions, request)

    def cancel(self, request, foptions):
        if request.get('subscriptionReferenceCode') is None:
            raise Exception('subscriptionReferenceCode must be in request')
        token = request.get('subscriptionReferenceCode')
        return self.connect('POST', '/v2/subscription/subscriptions/' + token + '/cancel', foptions, request)

    def detail(self, request, foptions):
        if request.get('subscriptionReferenceCode') is None:
            raise Exception('subscriptionReferenceCode must be in request')
        token = request.get('subscriptionReferenceCode')
        return self.connect('GET', '/v2/subscription/subscriptions/' + token, foptions, request)

    def orders(self, request, foptions):
        if request.get('subscriptionReferenceCode') is None:
            raise Exception('subscriptionReferenceCode must be in request')
        token = request.get('subscriptionReferenceCode')
        return self.connect('GET', '/v2/subscription/orders/' + token, foptions, request)

    def get(self, request, foptions):
        page = str(request.get('page') or 1)
        count = str(request.get('count') or 10)
        return self.connect('GET', '/v2/subscription/subscriptions/', foptions, request)

    def cardupdate(self, request, foptions):
        if request.get('subscriptionReferenceCode') is None:
            raise Exception('subscriptionReferenceCode must be in request')
        return self.connect('POST', '/v2/subscription/card-update/checkoutform/initialize/with-subscription', foptions, request)
