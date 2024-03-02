import json
import os

from django.core.management import BaseCommand

from core.models import Language


class Command(BaseCommand):
    help = "Creates Languages"

    def handle(self, *args, **kwargs):
        self.stdout.write("Languages insertion is started...")
        path = os.path.join(os.path.abspath(os.path.dirname("manage.py")), "core/management/commands/languages.json")
        f = open(path)
        data = json.load(f)
        Language.objects.bulk_create(
            [Language(name=language["Language name "], code=language["639-2/T "]) for language in data]
        )
        self.stdout.write("Languages insertion is completed...")
