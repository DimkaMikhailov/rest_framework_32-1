from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.models import *
from products.serializers import *


@api_view(['GET', 'POST'])
def products_list(request):
    if request.method == 'GET':
        products = Product.objects.select_related('category').prefetch_related('tags').all()
        json = ProductSerializer(products, many=True)
        return Response(data={"products": json.data}, status=status.HTTP_200_OK)
    elif request.method == 'POST' and request.data:
        serializer = ProductCreateValidSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={"product": "bad request", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        product = Product(**serializer.primitive)
        product.save()
        product.tags.set(serializer.collection.get('tags'))
        json = ProductSerializer(product)
        return Response(data={"products": json.data}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def product_detail(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)

        if request.method == 'GET' and product:
            json = ProductSerializer(product)
            return Response(status=status.HTTP_200_OK, data={'product': json.data})
        elif request.method in 'PATCH PUT'.split() and request.data:
            serializer = ProductUpdateValidSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(data={"product": "bad request", "error": serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
            for k, v in serializer.primitive.items():
                setattr(product, k, v)
            product.save()
            product.tags.set(serializer.collection.get('tags'))
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
        serializer = CategoryCreateUpdateValidSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={"category": "bad request", "error": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)

        category = Category.objects.create(name=serializer.validated_data.get('name'))
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
            serializer = CategoryCreateUpdateValidSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(data={"category": "bad request", "error": serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)
            category.name = serializer.validated_data.get('name', category.name)
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
        serializer = ReviewCreateValidSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(data={"review": "bad request", "error": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
        review = Review()
        review.product_id = serializer.validated_data.get('product_id')
        review.comment = serializer.validated_data.get('comment')
        review.starts = serializer.validated_data.get('stars', 1)
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
            serializer = ReviewUpdateValidSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(data={"review": "bad request", "error": serializer.errors},
                                status=status.HTTP_400_BAD_REQUEST)

            review.comment = serializer.validated_data.get('comment', review.comment)
            review.starts = serializer.validated_data.get('stars', review.starts)
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


@api_view(['GET'])
def tag_review(request):
    tag = Tag.objects.all()
    json = TagsSerializer(tag, many=True)

    return Response(data=json.data, status=status.HTTP_200_OK)
