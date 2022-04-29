# Заливка данных в базу из файлов .csv (api_yambd/static/data)
# необходима правка
import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand
from reviews import models as rev
from titles import models as tit
from users import models as use


class Command(BaseCommand):

    def handle(self, *args, **options):
        csv_data_files = (
            (use.User, 'users.csv'),
            (tit.Category, 'category.csv'),
            (tit.Genre, 'genre.csv'),
            (tit.Title, 'titles.csv'),
            (tit.GenreTitle, 'genre_title.csv'),
            (rev.Review, 'review.csv'),
            (rev.Comment, 'comments.csv'),
        )

        self.stdout.write(
            self.style.NOTICE(
                'Clearing Database...\n'
            )
        )

        for model, _ in reversed(csv_data_files):
            model.objects.all().delete()

        self.stdout.write(
            self.style.NOTICE(
                'Starting to add prepared data...\n'
            )
        )

        for model, filename in csv_data_files:
            filepath = os.path.join(
                settings.BASE_DIR, 'static/data', filename
            )

            self.stdout.write(
                self.style.NOTICE(
                    f'Processing file {filepath}\n'
                )
            )

            with open(filepath, newline='') as csv_file:
                csv_reader = csv.DictReader(csv_file)

                for row in csv_reader:
                    object_data = self.prepare_model_object_data(row)
                    obj = model.objects.get_or_create(**object_data)
                    self.stdout.write(self.style.SQL_FIELD(obj))

                self.stdout.write('\n')

        self.stdout.write(
            self.style.SUCCESS(
                'Database has been filled successfully!'
            )
        )

    def prepare_model_object_data(self, csv_row_dict):
        foreign_keys = {
            'category': (tit.Category, 'category'),
            'title_id': (tit.Title, 'title'),
            'genre_id': (tit.Genre, 'genre'),
            'author': (use.User, 'author'),
            'review_id': (rev.Review, 'review')
        }

        object_data = {}

        for column, value in csv_row_dict.items():
            if column in foreign_keys:
                (model, field_name) = foreign_keys[column]
                obj = model.objects.get(pk=csv_row_dict[column])
                object_data[field_name] = obj
            else:
                object_data[column] = value

        return object_data
