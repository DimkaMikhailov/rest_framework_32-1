from django.urls import path
from products.views import *

urlpatterns = [
    path('products/', ProductListCreateAPIView.as_view()),
    path('products/<int:id>/', ProductRetrieveUpdateDestroyAPIView.as_view()),
    path('products/reviews/', ProductReviewListAPIView.as_view()),
    path('categories/', CategoryViewSet.as_view({
        'post': 'create',
        'get': 'list'
    })),
    path('categories/<int:id>/', CategoryViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'delete'
    })),
    path('reviews/', ReviewViewSet.as_view({
        'get': 'list',
        'post': 'create'
    })),
    path('reviews/<int:id>/', ReviewViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'patch': 'partial_update',
        'delete': 'delete'
    })),
    path('tags/', TagListAPIView.as_view()),
]
