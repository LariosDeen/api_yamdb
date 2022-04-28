from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MyTokenObtainPairView, SignUpViewSet

app_name = "api"

router = DefaultRouter()
router.register('signup', SignUpViewSet, basename='signup')

urlpatterns = [
    path('v1/auth/', include(router.urls)),
    path('v1/auth/token/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),
]
