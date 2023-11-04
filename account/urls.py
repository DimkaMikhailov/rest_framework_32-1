from django.urls import path
from account.views import *

urlpatterns = [
    path('api/v1/login/', login_api_view),
    path('api/v1/register/', register_api_view),
    path('api/v1/users/confirm/', confirm_api_view),
]
