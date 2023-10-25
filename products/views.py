from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import *
from products.serializers import *


@api_view(['GET', 'POST'])
def products_list(request):
    if request.method == 'GET':
        products = Product.objects.select_related('category').all()
        json = ProductSerializer(products, many=True)
        return Response(data={"products": json.data}, status=status.HTTP_200_OK)
    elif request.method == 'POST' and request.data:
        products = Product()
        products.title = request.data.get('title')
        products.description = request.data.get('description')
        products.price = request.data.get('price')
        products.category_id = request.data.get('category_id')
        products.save()
        json = ProductSerializer(products)
        return Response(data={"products": json.data}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_detail(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)

        if request.method == 'GET' and product:
            json = ProductSerializer(product)
            return Response(status=status.HTTP_200_OK, data={'product': json.data})
        elif request.method in 'PATCH PUT'.split() and request.data:
            product.title = request.data.get('title', product.title)
            product.description = request.data.get('description', product.description)
            product.price = request.data.get('price', product.price)
            product.category_id = request.data.get('category_id', product.category_id)
            product.save()
            json = ProductSerializer(product)
            return Response(status=status.HTTP_201_CREATED, data={'message': f'{product.pk} updated', 'product': json.data})
        elif request.method == 'DELETE':
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data={'message': f'{product_id=} deleted'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def categories_list(request):
    if request.method == 'GET':
        categories = Category.objects.prefetch_related('product').all()
        json = CategoryDetailSerializer(categories, many=True)
        return Response(data={'categories': json.data}, status=status.HTTP_200_OK)
    elif request.method == 'POST' and request.data:
        category = Category.objects.create(name=request.data.get('name'))
        json = CategorySerializer(category)
        return Response(status=status.HTTP_201_CREATED, data={'category': json.data})
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def category_view(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)

        if request.method == 'GET':
            json = CategoryDetailSerializer(category)
            return Response(data={'category': json.data}, status=status.HTTP_200_OK)
        elif request.method in 'PUT PATCH'.split() and request.data:
            category.name = request.data.get('name', category.name)
            category.save()
            json = CategoryDetailSerializer(category)
            return Response(data={'message': 'updated', 'category': json.data})
        elif request.method == 'DELETE':
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data={'message': f'{category_id=} deleted'})
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def reviews_list(request):
    if request.method == 'GET':
        reviews = Review.objects.select_related('product').all()
        json = ReviewListSerializer(reviews, many=True)
        return Response(data={'reviews': json.data}, status=status.HTTP_200_OK)
    elif request.method == 'POST' and request.data:
        review = Review()
        review.product_id = request.data.get('product_id')
        review.comment = request.data.get('comment')
        review.starts = request.data.get('stars', 1)
        review.save()
        json = ReviewSerializer(review)
        return Response(data={'message': f"{review.pk} created", 'review': json.data}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def review_detail(request, review_id):
    try:
        review = Review.objects.get(pk=review_id)

        if request.method == 'GET':
            json = ReviewSerializer(review)
            return Response(data=json.data, status=status.HTTP_200_OK)
        elif request.method in ['PUT', 'PATCH'] and request.data:
            review.comment = request.data.get('comment', review.comment)
            review.starts = request.data.get('stars', review.starts)
            review.save()
            json = ReviewSerializer(review)
            return Response(data={'message': f"{review_id=} updated", 'review': json.data})
        elif request.method == 'DELETE':
            review.delete()
            return Response(data={'message': f"{review_id=} deleted"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def products_reviews(request):
    p = Product.objects.select_related('category').prefetch_related('reviews').all()
    json = ProductsReviewsSerializer(p, many=True)
    return Response(data=json.data, status=status.HTTP_200_OK)
