from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import *
from products.serializers import *


@api_view(['GET'])
def products_list(request):
    products = Product.objects.all()
    json = ProductSerializer(products, many=True)
    return Response(data=json.data)


@api_view(['GET'])
def product_detail(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        json = ProductSerializer(product)
        return Response(data=json.data, status=status.HTTP_200_OK)

    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def categories_list(request):
    categories = Category.objects.all()
    json = CategorySerializer(categories, many=True)
    return Response(data=json.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def category_view(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
        json = CategorySerializer(category)
        return Response(data=json.data, status=status.HTTP_200_OK)

    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def reviews_list(request):
    reviews = Review.objects.all()
    json = ReviewSerializer(reviews, many=True)
    return Response(data=json.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def review_detail(request, review_id):
    try:
        reviews = Review.objects.get(pk=review_id)
        json = ReviewSerializer(reviews)
        return Response(data=json.data, status=status.HTTP_200_OK)

    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

