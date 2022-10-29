import json

from django.core.management.base import BaseCommand, CommandError

from recipes.ingredients.models import Ingredient

PATH_JSON_INGREDIENTS = ''


class Command(BaseCommand):
    help = 'Загрузка ингредиентов в БД'

    def handle(self, *args, **options):
        with open(PATH_JSON_INGREDIENTS, encoding='utf-8') as data_file:
            json_data = json.loads(data_file.read())
        Ingredient.objects.bulk_create(
            (
                Ingredient(
                    name=ingredient['name'], measurement_unit=ingredient['measurement_unit']
                ) for ingredient in json_data
            ),
            ignore_conflicts=True
        )
        self.stdout.write(self.style.SUCCESS('Ингредиенты успешно загружены в БД!'))
