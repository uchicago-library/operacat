
import json
from django.core.management.base import BaseCommand
from wagtail.core.models import Page

from catalogitems.models import Composer, CatalogItemPage

class Command(BaseCommand):
    """a management command to create initial migration of items from legacy data

    This class is necessary for a starting the migration of legacy data into the system.
    """
    help = "Add item pages for every item in legacy data to system"

    def add_arguments(self, parser):
        """the method that gets called to add parameter to the management command

        It takes a parser object and adds a string type argument called
        legacy_data_filepath
        """
        parser.add_argument("legacy_data_filepath",
                            help="Path to legacy data JSON", type=str)

    def handle(self, *args, **options):
        """the method that gets called to actually run the management command

        It opens the legacy_data_filepath parameter and loads it into a JSON
        object

        Then it iterates through the list of dicts in the data and selects
        out the item key:value.

        It then checks if there is a CatalogItemPage already present with that item
        in the title, and if ther is not it creates one and adds it to the system
        as a child of the home page.
        """
        data = json.load(open(options["legacy_data_filepath"], "r",
                              encoding="utf-8"))
        for n_item in data:
            new_composer = n_item["composer"]
            print(new_composer)
            if new_composer != 'None':
                check_for_existing_record = Composer.objects.filter(last_name=new_composer.split(',')[0])
                if check_for_existing_record.count() == 0:
                    print(new_composer)
                    new = Composer()
                    new.last_name = new_composer.split(',')[0]
                    new.first_name = new_composer.split(',')[1]
                    new.save()
                else:
                    new = check_for_existing_record[0]
                    self.stderr.write("{} already exists in database.\n".format(new_composer))
            cur = CatalogItemPage.objects.filter(title=n_item["IdNumber"])
            if cur.count() == 1:
                cur = cur[0]
                cur.item_composer = new
                cur.save()
