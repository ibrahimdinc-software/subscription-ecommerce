from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from rest_framework import generics
from rest_framework import mixins

from rest_framework.response import Response


from .serializers import OrderStatusSerializer, PaymentMethodsSerializer, OrderDetailsSerializer, OrdersSerializer
from .models import OrderStatus, PaymentMethods, OrderDetailsModel, Orders


from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import authentication
from rest_framework import exceptions

# Create your views here.


class SimpleAuthentication(authentication.BaseAuthentication):
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token

    def authenticate(self, request):
        auth = request.headers.get("token")
        print(auth)
        if not auth:
            return None

        return self.authenticate_credentials(auth)

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(
                _('User inactive or deleted.'))

        return (token.user, token)


class OrderStatusGenericView(generics.GenericAPIView,  mixins.ListModelMixin):

    serializer_class = OrderStatusSerializer
    queryset = OrderStatus.objects.all()

    authentication_classes = [SimpleAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"OrderStatus": self.list(request).data})


class PaymentMethodsGenericView(generics.GenericAPIView,  mixins.ListModelMixin):

    serializer_class = PaymentMethodsSerializer
    queryset = PaymentMethods.objects.all()

    authentication_classes = [SimpleAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return self.list(request)


class OrderDetailsGenericView(generics.GenericAPIView,  mixins.ListModelMixin):

    serializer_class = OrderDetailsSerializer
    queryset = OrderDetailsModel.objects.all()

    authentication_classes = [SimpleAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return self.list(request)


class OrdersGenericView(generics.GenericAPIView,  mixins.ListModelMixin):

    serializer_class = OrdersSerializer
    queryset = Orders.objects.all()

    authentication_classes = [SimpleAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({"Orders": self.list(request).data})
