from rest_framework import serializers
from .models import Conversation, HandShake, ItemTransactions


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        exclude = ['order', 'is_pay']


class ItemTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemTransactions
        fields = '__all__'


class HandShakeSerializer(serializers.ModelSerializer):
    itemTransactions = ItemTransactionSerializer(many=True)

    class Meta:
        model = HandShake
        exclude = ['conversation']

    def create(self, validated_data):
        itemTransactions_data = validated_data.pop('itemTransactions')

        handShake = HandShake.objects.create(**validated_data)
        it_id = []
        for it in itemTransactions_data:
            it.pop('convertedPayout')
            it = ItemTransactions.objects.create(**it)

            it_id.append(it.id)

        handShake.itemTransactions.set(it_id)

        return handShake
