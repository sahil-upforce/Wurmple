from django.core.management import BaseCommand

from core.models import Category


class Command(BaseCommand):
    help = "Creates Categories"

    def handle(self, *args, **kwargs):
        self.stdout.write("Categories insertion is started...")
        categories_list = [
            {"name": "Mountains", "code": "MNT"},
            {"name": "Forests", "code": "FRST"},
            {"name": "Beaches", "code": "BCS"},
            {"name": "Islands", "code": "ISLNDS"},
            {"name": "Deserts", "code": "DSRTS"},
            {"name": "Lakes", "code": "LKS"},
            {"name": "Rivers", "code": "RVRS"},
            {"name": "Waterfalls", "code": "WTRFLS"},
            {"name": "Caves", "code": "CVS"},
            {"name": "Canyons", "code": "CNYNS"},
            {"name": "Reefs", "code": "RFS"},
            {"name": "Glaciers", "code": "GLCRS"},
            {"name": "Cities", "code": "CTS"},
            {"name": "Towns", "code": "TWNS"},
            {"name": "Villages", "code": "VLGS"},
            {"name": "Historical Sites", "code": "HSTRCL"},
            {"name": "Religious Sites", "code": "RLGS"},
            {"name": "Parks", "code": "PRKS"},
            {"name": "Gardens", "code": "GRDNS"},
            {"name": "Farms", "code": "FRMS"},
            {"name": "Factories", "code": "FCTRS"},
            {"name": "Power Plants", "code": "PWRPLNTS"},
            {"name": "Dams", "code": "DMS"},
            {"name": "Bridges", "code": "BRDGS"},
            {"name": "Tunnels", "code": "TNLS"},
            {"name": "Skyscrapers", "code": "SKYSCRPR"},
            {"name": "National Parks", "code": "NTNLPRKS"},
            {"name": "Amusement Parks", "code": "AMSMNTPRKS"},
            {"name": "Museums", "code": "MSMS"},
            {"name": "Libraries", "code": "LBRRS"},
        ]
        Category.objects.bulk_create(
            [Category(name=category["name"], code=category["code"]) for category in categories_list]
        )
        self.stdout.write("Categories insertion is completed...")
