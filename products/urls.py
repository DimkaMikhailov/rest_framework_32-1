from django.urls import path
from products.views import *

urlpatterns = [
    path('api/v1/products/', products_list),
    path('api/v1/products/<int:product_id>/', product_detail),
    path('api/v1/categories/', categories_list),
    path('api/v1/categories/<int:category_id>/', category_view),
    path('api/v1/reviews/', reviews_list),
    path('api/v1/reviews/<int:review_id>/', review_detail),
    path('api/v1/products/reviews/', products_reviews),
    path('api/v1/tag/', tag_review),
]
