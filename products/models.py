from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @property
    def products_count(self):
        return self.product.count()


class Product(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=3, default='$')
    in_stock = models.BooleanField(default=True)

    category = models.ForeignKey(to=Category, on_delete=models.DO_NOTHING, related_name='product')

    def __str__(self):
        return self.title

    @property
    def rating(self):
        reviews = self.reviews.all()
        _sum = sum([r.starts for r in reviews])
        return round(_sum / len(reviews), 3) if 0 < _sum > len(reviews) else 0


STARS = (
            (1, '⭐'),
            (2, '⭐' * 2),
            (3, '⭐' * 3),
            (4, '⭐' * 4),
            (5, '⭐' * 5),
        )


class Review(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.DO_NOTHING, related_name='reviews')

    comment = models.TextField()
    starts = models.IntegerField(choices=STARS, default=1)

    def __str__(self):
        return self.comment
