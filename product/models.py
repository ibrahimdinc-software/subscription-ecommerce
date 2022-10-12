from django.db import models
from django.utils.text import slugify
# Create your models here.


class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.CharField("", max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def get_products(self):
        return ProductModel.objects.filter(category=self).order_by("name")

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # Call the real save() method
        super(CategoryModel, self).save(*args, **kwargs)


class ProductModel(models.Model):
    name = models.CharField(verbose_name="Ürün Adı", max_length=100)
    code = models.CharField(verbose_name="Ürün Kodu",
                            max_length=100)
    category = models.ForeignKey(
        CategoryModel, on_delete=models.CASCADE, blank=True, null=True)

    unit_price = models.FloatField(
        verbose_name="Birim Fiyatı (KDV'SİZ)", blank=True, null=True)
    price = models.FloatField(verbose_name="Satış Fiyatı")
    vat_rate = models.IntegerField(verbose_name="KDV Oranı")

    picture = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.unit_price = self.price / (self.vat_rate / 100 + 1)
        # Call the real save() method
        super(ProductModel, self).save(*args, **kwargs)

    def is_picture(self):
        if self.picture:
            return True
        return False
