# Generated by Django 4.1.2 on 2022-10-12 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productmodel',
            name='code',
            field=models.CharField(max_length=100, verbose_name='Ürün Kodu'),
        ),
    ]