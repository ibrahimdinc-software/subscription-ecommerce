from rest_framework import serializers
from .models import OrderStatus, PaymentMethods, Orders, OrderDetailsModel


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'
        #exclude = ["order"]


class PaymentMethodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethods
        fields = '__all__'


class OrderDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderDetailsModel
        fields = '__all__'


class OrdersSerializer(serializers.ModelSerializer):
    OrderDetails = OrderDetailsSerializer(many=True)

    class Meta:
        model = Orders
        fields = '__all__'

    def create(self, validated_data):
        orderDetails_data = validated_data.pop('OrderDetails')
        o = Orders.objects.create(**validated_data)
        od_id = []
        for od in orderDetails_data:
            od = OrderDetailsModel.objects.create(**od)
            print(od)
            od_id.append(od.pk)

        o.OrderDetails.set(od_id)

        return o
