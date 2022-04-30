from rest_framework import serializers

from reviews.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date',)
