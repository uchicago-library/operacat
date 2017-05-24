
from django.core.management.base import BaseCommand, CommandError
from catalogitems.models import CatalogItemPage, Place, Dealer,\
 Composer, AuthorOrResponsible, RecipientOrDedicatee
import json
from os.path import dirname, join

class Command(BaseCommand):
    help = "Add related item info from legacy data to new OperaCat website"

    def add_arguments(self, parser):
        parser.add_argument("legacy_data_filepath",
                            help="Path to legacy data JSON", type=str)

    def handle(self, *args, **options):
        data = json.load(open(options["legacy_data_filepath"], "r",
                              encoding="utf-8"))
        successful = open(join(dirname(options["legacy_data_filepath"]),
                               'successful.txt'), "w")
        for n in data:
            cur = CatalogItemPage.objects.filter(title=n["item"])
            if cur.count() == 1:
               cur = cur[0]
               if n.get("item description", None):
                   val = n["item description"]
                   cur.item_description = "<p>" + val.strip() + "</p>"
               if n.get("item notes", None):
                   val = n["item notes"]
                   cur.field_notes = "<p>" + val.strip() + "</p>"
                   print(cur.title)
                   print(cur.field_notes.encode('utf-8'))
               cur.save()