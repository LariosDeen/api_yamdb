from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Review, Comment
from reviews.serializers import ReviewSerializer, CommentSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
