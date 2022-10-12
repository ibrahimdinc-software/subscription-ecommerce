# Generated by Django 3.0.2 on 2020-08-29 14:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subscription', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='pricingplanmodel',
            name='pricing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription.PricingModel', verbose_name='Fiyatlandırma'),
        ),
        migrations.AddField(
            model_name='pricingmodel',
            name='features',
            field=models.ManyToManyField(blank=True, to='subscription.PricingFeatureModel'),
        ),
        migrations.AddField(
            model_name='pricingmodel',
            name='products',
            field=models.ManyToManyField(blank=True, to='product.ProductModel'),
        ),
        migrations.AddField(
            model_name='pricingmodel',
            name='secondaryProducts',
            field=models.ManyToManyField(blank=True, related_name='sproduct', to='product.ProductModel'),
        ),
        migrations.AddField(
            model_name='cancelsubscription',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription.SubscriptionModel'),
        ),
        migrations.AddField(
            model_name='cancelsubscription',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
