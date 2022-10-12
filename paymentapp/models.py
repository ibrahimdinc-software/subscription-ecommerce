from django.db import models

from order.models import OrderModel


# Create your models here.


class Conversation(models.Model):
    conversationId = models.CharField(max_length=100, primary_key=True)
    status = models.CharField(max_length=100)
    paymentId = models.CharField(max_length=100)
    conversationData = models.CharField(max_length=100, blank=True, null=True)
    order = models.ForeignKey(
        "order.OrderModel", on_delete=models.CASCADE, blank=True, null=True)
    is_pay = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.conversationId

    def save(self, *args, **kwargs):
        if not self.order:
            self.order = OrderModel.objects.get(pk=int(self.conversationId))
        # Call the real save() method
        super(Conversation, self).save(*args, **kwargs)


class ItemTransactions(models.Model):
    paymentTransactionId = models.CharField(
        max_length=200, blank=True, null=True)
    itemId = models.CharField(max_length=200, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    paidPrice = models.FloatField(blank=True, null=True)
    transactionStatus = models.IntegerField(blank=True, null=True)
    blockageRate = models.FloatField(blank=True, null=True)
    blockageRateAmountMerchant = models.FloatField(blank=True, null=True)
    blockageRateAmountSubMerchant = models.FloatField(blank=True, null=True)
    blockageResolvedDate = models.CharField(
        max_length=200, blank=True, null=True)
    subMerchantPrice = models.FloatField(blank=True, null=True)
    subMerchantPayoutRate = models.FloatField(blank=True, null=True)
    subMerchantPayoutAmount = models.IntegerField(blank=True, null=True)
    iyziCommissionFee = models.FloatField(blank=True, null=True)
    iyziCommissionRateAmount = models.FloatField(blank=True, null=True)
    merchantCommissionRate = models.FloatField(blank=True, null=True)
    merchantCommissionRateAmount = models.FloatField(blank=True, null=True)
    merchantPayoutAmount = models.FloatField(blank=True, null=True)


class HandShake(models.Model):
    conversationId = models.CharField(max_length=100, primary_key=True)
    status = models.CharField(max_length=100)
    locale = models.CharField(max_length=100)
    systemTime = models.BigIntegerField()
    installment = models.IntegerField(blank=True, null=True)
    errorCode = models.CharField(max_length=200, blank=True, null=True)
    errorMessage = models.CharField(max_length=200, blank=True, null=True)
    errorGroup = models.CharField(max_length=200, blank=True, null=True)
    paymentId = models.CharField(max_length=100, blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    paidPrice = models.FloatField(blank=True, null=True)
    basketId = models.CharField(max_length=200, blank=True, null=True)
    currency = models.CharField(max_length=200, blank=True, null=True)
    binNumber = models.CharField(max_length=200, blank=True, null=True)
    lastFourDigits = models.CharField(max_length=200, blank=True, null=True)
    cardAssociation = models.CharField(max_length=200, blank=True, null=True)
    cardFamily = models.CharField(max_length=200, blank=True, null=True)
    cardType = models.CharField(max_length=200, blank=True, null=True)
    authCode = models.CharField(max_length=200, blank=True, null=True)
    phase = models.CharField(max_length=200, blank=True, null=True)
    mdStatus = models.IntegerField()
    hostReference = models.CharField(max_length=200, blank=True, null=True)
    fraudStatus = models.BooleanField(blank=True, null=True)
    iyziCommissionFee = models.FloatField(blank=True, null=True)
    iyziCommissionRateAmount = models.FloatField(blank=True, null=True)
    merchantCommissionRate = models.FloatField(blank=True, null=True)
    merchantCommissionRateAmount = models.FloatField(blank=True, null=True)
    itemTransactions = models.ManyToManyField(
        ItemTransactions)
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.conversation = Conversation.objects.get(pk=self.conversationId)
        # Call the real save() method
        super(HandShake, self).save(*args, **kwargs)
