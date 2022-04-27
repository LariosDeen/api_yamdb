from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import SignUp, MyTokenObtainPairView

app_name = "api"

urlpatterns = [
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path('v1/token/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
