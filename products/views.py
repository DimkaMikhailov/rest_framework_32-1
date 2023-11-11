from products.models import *
from products.serializers import (ProductSerializer,
                                  ProductCreateValidSerializer,
                                  ProductUpdateValidSerializer,
                                  ProductsReviewsSerializer,
                                  CategoryDetailSerializer,
                                  CategoryCreateUpdateValidSerializer,
                                  ReviewListSerializer,
                                  ReviewCreateValidSerializer,
                                  ReviewUpdateValidSerializer,
                                  TagsSerializer)
from custom.views import (CustomListCreateAPIView,
                          CustomRetrieveUpdateDestroyAPIView,
                          CustomModelViewSet,
                          CustomListAPIView)


class ProductListCreateAPIView(CustomListCreateAPIView):
    """
    View for handling product creation and listing.
    """
    model = Product
    prefetch = 'tags'
    select = 'category'
    list_serializer = ProductSerializer
    create_serializer = ProductCreateValidSerializer


class ProductRetrieveUpdateDestroyAPIView(CustomRetrieveUpdateDestroyAPIView):
    model = Product
    lookup_field = 'id'
    retrieve_serializer = ProductSerializer
    update_serializer = ProductUpdateValidSerializer


class CategoryViewSet(CustomModelViewSet):
    model = Category
    prefetch = 'product'
    lookup_field = 'id'
    list_serializer = CategoryDetailSerializer
    create_serializer = CategoryCreateUpdateValidSerializer
    retrieve_serializer = CategoryDetailSerializer
    update_serializer = CategoryCreateUpdateValidSerializer


class ReviewViewSet(CustomModelViewSet):
    model = Review
    select = 'product'
    lookup_field = 'id'
    list_serializer = ReviewListSerializer
    create_serializer = ReviewCreateValidSerializer
    retrieve_serializer = ReviewListSerializer
    update_serializer = ReviewUpdateValidSerializer


class ProductReviewListAPIView(CustomListAPIView):
    model = Product
    select = 'category'
    prefetch = 'reviews'
    list_serializer = ProductsReviewsSerializer


class TagListAPIView(CustomListAPIView):
    model = Tag
    list_serializer = TagsSerializer
