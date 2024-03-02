import json
import os

from django.core.management import BaseCommand

from core.models import City, Country, State


class Command(BaseCommand):
    help = "Creates Cities"

    def handle(self, *args, **kwargs):
        self.stdout.write("Cities insertion is started...")
        path = os.path.join(os.path.abspath(os.path.dirname("manage.py")), "core/management/commands/cities.json")
        f = open(path)
        data = json.load(f)
        for i in data:
            try:
                country, created = Country.objects.update_or_create(name=i["country_name"], code=i["country_code"])
                state, created = State.objects.update_or_create(
                    name=i["state_name"], code=i["state_code"], country=country
                )
                city, created = City.objects.update_or_create(name=i["name"], code=i["name"], state=state)
            except Exception:
                continue
        self.stdout.write("Cities insertion is completed...")
