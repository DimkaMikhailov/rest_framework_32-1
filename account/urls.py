from django.urls import path
from account.views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('register/', RegisterCreateAPIView.as_view()),
    path('users/confirm/', ConfirmLoginAPIView.as_view()),
]
