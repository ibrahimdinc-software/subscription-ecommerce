# Generated by Django 3.0.2 on 2020-08-29 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CancelSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.CharField(choices=[('0', 'Onay Bekliyor'), ('1', 'Onaylandı'), ('2', 'Reddedildi')], default='0', max_length=20, verbose_name='Durum')),
                ('description', models.CharField(blank=True, max_length=140, null=True, verbose_name='Açıklama')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Tarih')),
                ('order_cancel', models.BooleanField(default=False, verbose_name='Sipariş İptal Edildi Mi?')),
            ],
        ),
        migrations.CreateModel(
            name='PricingFeatureModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('order', models.IntegerField(verbose_name='Gösterme Sırası')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='PricingModel',
            fields=[
                ('name', models.CharField(max_length=155)),
                ('code', models.CharField(max_length=55, primary_key=True, serialize=False, unique=True)),
                ('first_price', models.FloatField()),
                ('discount', models.FloatField()),
                ('picture', models.FileField(blank=True, null=True, upload_to='')),
                ('pricing_type', models.CharField(choices=[('0', 'Abonelik'), ('1', 'Hediye'), ('2', 'Özel')], max_length=8, verbose_name='Paket Türü')),
                ('order', models.IntegerField(verbose_name='Gösterme Sırası')),
                ('referenceCode', models.CharField(blank=True, max_length=500, null=True, verbose_name='iyzico referans')),
            ],
        ),
        migrations.CreateModel(
            name='PricingPlanModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='İsim')),
                ('interval', models.CharField(choices=[('DAILY', 'Günlük'), ('WEEKLY', 'Haftalık'), ('MONTHLY', 'Aylık')], max_length=30, verbose_name='Aralık')),
                ('frequency', models.IntegerField(verbose_name='Sıklık')),
                ('referenceCode', models.CharField(blank=True, max_length=100, null=True, verbose_name='iyzico referans')),
            ],
        ),
        migrations.CreateModel(
            name='SubscriptionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Tarih')),
                ('price', models.FloatField(verbose_name='Fiyat')),
                ('status', models.CharField(choices=[('0', 'Pasif'), ('1', 'Aktif')], max_length=30, verbose_name='Abonelik Durumu')),
                ('discount', models.FloatField(verbose_name='Abonelik İndirimi')),
                ('referenceCode', models.CharField(max_length=100)),
                ('pricing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription.PricingPlanModel')),
            ],
        ),
    ]
