from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import MyTokenObtainPairView, SignUpViewSet, UsersViewSet
from titles.views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = "api"

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('auth/signup', SignUpViewSet, basename='signup')
router.register('users', UsersViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),

]
