from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from reviews.views import ReviewViewSet, CommentViewSet
from .views import MyTokenObtainPairView, SignUpViewSet, UsersViewSet
from titles.views import CategoryViewSet, GenreViewSet, TitleViewSet

app_name = "api"

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('auth/signup', SignUpViewSet, basename='signup')
router.register('users', UsersViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', MyTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/auth/token/refresh/',
         TokenRefreshView.as_view(),
         name='token_refresh'),

]
