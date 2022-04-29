from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import Me, MyTokenObtainPairView, SignUpViewSet, UsersViewSet

app_name = "api"

router = DefaultRouter()
router.register('auth/signup', SignUpViewSet, basename='signup')
router.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path('v1/users/me/', Me.as_view()),
    path('v1/', include(router.urls)),
    path('v1/auth/token/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),

]
