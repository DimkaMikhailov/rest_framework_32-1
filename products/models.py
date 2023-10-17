from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=3, default='$')
    in_stock = models.BooleanField(default=True)

    category = models.ForeignKey(to=Category, on_delete=models.DO_NOTHING, related_name='product')

    def __str__(self):
        return self.title


class Review(models.Model):
    comment = models.TextField()

    product = models.ForeignKey(to=Product, on_delete=models.DO_NOTHING, related_name='review')

    def __str__(self):
        return self.comment
