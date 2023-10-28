from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from products.models import Product, Category, Review, Tag


# --------------------------------CATEGORIES--------------------------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class CategoryDetailSerializer(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['products_count']


class CategoryCreateUpdateValidSerializer(serializers.Serializer):
    name = serializers.CharField()

    def validate_name(self, name):
        categories = list(Category.objects.values_list('name', flat=True))
        print(categories)
        if name in categories:
            raise ValidationError(f'{name=} already in collection')
        return name


# --------------------------------TAGS--------------------------------------

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


# --------------------------------REVIEWS--------------------------------------

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


class ReviewCreateValidSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(min_value=1)
    comment = serializers.CharField(min_length=10, max_length=500)
    stars = serializers.IntegerField(min_value=1, max_value=5, required=False, default=1)

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError('product id not in collection')
        return product_id

    def validate_comment(self, text):
        invalid = set(text.lower().split())
        ban_words = ['bitch', 'fuck', 'shirt', 'fuck,', 'bitch,']

        for words in ban_words:
            if words in invalid:
                raise ValidationError('incorrect comment')
        return text


class ReviewUpdateValidSerializer(ReviewCreateValidSerializer):
    stars = serializers.IntegerField(min_value=1, max_value=5, required=False, default=1)
    comment = serializers.CharField(max_length=500, required=False)


# --------------------------------PRODUCT--------------------------------------


class ProductSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()
    # tags = TagsSerializer(many=True)

    def get_tags(self, product):
        return [tag.name for tag in product.tags.all()]

    class Meta:
        model = Product
        fields = 'id title description price currency tags'.split()


class ProductsReviewsSerializer(ProductSerializer):
    reviews = ReviewSerializer(many=True)

    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ['reviews', 'rating']


class ProductCreateValidSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=10, max_length=100)
    description = serializers.CharField(min_length=10)
    price = serializers.FloatField(min_value=0.0)
    category_id = serializers.IntegerField(min_value=1)
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))

    @property
    def primitive(self):
        return {k: v for k, v in self.validated_data.items() if isinstance(v, (str, int, float, bool))}

    @property
    def collection(self):
        return {k: v for k, v in self.validated_data.items() if isinstance(v, (list | tuple | dict))}

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise ValidationError('category_id dose not exist')
        return category_id

    def validate_tags(self, tags):
        valid_tags = list(Tag.objects.values_list('id', flat=True))
        if error_index := [tags.index(i) for i in tags if i not in valid_tags]:
            e = ValidationError()
            for er in error_index:
                e.detail.append({f'tag[{er}]': 'Not in tag collection'})
            raise e
        return tags


class ProductUpdateValidSerializer(ProductCreateValidSerializer):
    title = serializers.CharField(min_length=10, max_length=100, required=False)
    description = serializers.CharField(min_length=10, required=False)
    price = serializers.FloatField(min_value=0.0, required=False)
    category_id = serializers.IntegerField(min_value=1, required=False)
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1), required=False)
