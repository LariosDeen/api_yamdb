from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# from django.contrib.auth import get_user_model
#
#
# User = get_user_model()
#
#
# class Title(models.Model):
#     text = models.TextField(max_length=500, verbose_name='Текст произведения')


class Review(models.Model):
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Название произведения'
    )
    text = models.TextField(max_length=500, verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.IntegerField (
        default=5,
        validators=[
            MinValueValidator(limit_value=1, message='Минимальная оценка 1'),
            MaxValueValidator(limit_value=10, message='Максимальная оценка 10')
        ],
        verbose_name='Оценка произведения'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации отзыва'
    )

    def __str__(self):
        return self.text[:10]

    class Meta:
        ordering = ['id']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title_id', 'author'], name='unique_review_author'
            )
        ]


class Comment(models.Model):
    review_id = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Комментарий к отзыву'
    )
    text = models.TextField(max_length=500, verbose_name='Текст комментария')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор комментария к отзыву'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации комментария'
    )

    def __str__(self):
        return self.text[:10]

    class Meta:
        ordering = ['id']
        verbose_name = 'Комментарий к отзывам'
        verbose_name_plural = 'Комментарии к отзывам'
