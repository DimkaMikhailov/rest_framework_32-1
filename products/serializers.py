from rest_framework import serializers
from products.models import Product, Category, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategoryDetailSerializer(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['products_count']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'comment']


class ReviewListSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    review_id = serializers.SerializerMethodField()

    def get_review_id(self, review):
        return review.pk

    def get_product(self, review):
        return review.product.title

    class Meta:
        model = Review
        fields = 'review_id comment product'.split()[::-1]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = 'id title description price currency category'.split()


class ProductsReviewsSerializer(ProductSerializer):
    reviews = ReviewSerializer(many=True)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['reviews', 'rating']
