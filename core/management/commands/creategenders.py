from django.core.management import BaseCommand

from user_app.models import Gender


class Command(BaseCommand):
    help = "Creates Genders"

    def handle(self, *args, **kwargs):
        self.stdout.write("Gender insertion is started...")
        gender_list = [
            {"name": "Male", "code": "ML"},
            {"name": "Female", "code": "FM"},
            {"name": "Others", "code": "OTH"},
        ]
        Gender.objects.bulk_create([Gender(name=gender["name"], code=gender["code"]) for gender in gender_list])
        self.stdout.write("Gender insertion is completed...")
