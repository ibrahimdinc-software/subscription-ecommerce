# Generated by Django 3.0.2 on 2020-08-29 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyCatModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Kedi Adı')),
                ('gender', models.CharField(choices=[('0', 'Dişi'), ('1', 'Erkek')], max_length=6, verbose_name='Cinsiyet')),
                ('status', models.CharField(choices=[('0', 'Yavru'), ('1', 'Yetişkin'), ('2', 'Kısırlaştırılmış')], max_length=20, verbose_name='Durumu')),
                ('spec_case', models.TextField(blank=True, max_length=140, null=True, verbose_name='Özel Durum')),
                ('picture', models.ImageField(upload_to='', verbose_name='Fotoğraf')),
            ],
        ),
    ]