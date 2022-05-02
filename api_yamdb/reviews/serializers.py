from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from rest_framework.fields import CreateOnlyDefault
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )
    class Meta:
        model = Review
        exclude = ('title',)
        # read_only_fields = ('author',)

    def validate(self, data):
        request = self.context.get('request')
        if request.method == 'POST':
            if self.context['request'].user == AnonymousUser:
                pass
            title_id = self.context['view'].kwargs.get('title_id'),
            author = self.context['request'].user
            if Review.objects.filter(title=title_id, author=author).exists():
                raise serializers.ValidationError(
                    'Вы уже оставили отзыв на этот обзор.'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        exclude = ('review',)
