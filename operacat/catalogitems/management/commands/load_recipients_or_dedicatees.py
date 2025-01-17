
import json
from django.core.management.base import BaseCommand
from wagtail.core.models import Page
import re

from catalogitems.models import RecipientOrDedicatee, CatalogItemPage

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
            new_recipients = n_item["recipientOrDedicatee"]
            if new_recipients != None:
                new_recipients = re.sub(r'\{|\}|\[|\]|\?', '', new_recipients)
                new_recipients = re.split(r'\;', new_recipients)
                new_recipients = [x.strip().lstrip() for x in new_recipients]
                new_recipients = [x for x in new_recipients if 'etc' not in x]
                new_recipients = [x for x in new_recipients if x != 'None']
                a_list = []
                for a_name in new_recipients:
                    check_for_existing_record = RecipientOrDedicatee.objects.filter(recipient_name=a_name)
                    if check_for_existing_record.count() == 0:
                        new = RecipientOrDedicatee()
                        new.recipient_name = a_name
                        new.save()
                    else:
                        self.stderr.write("{} already exists in database.\n".format(a_name))
            cur = CatalogItemPage.objects.filter(title=n_item["IdNumber"])
            if cur.count() == 1:
                cur = cur[0]
                print(cur.title)
                for n_recipient in a_list:
                    a = RecipientOrDedicatee.objects.filter(recipient_name=\
                                                            n_recipient)[0]
                    cur.item_recipientordedicatees.create(a_recipient=a)
                    cur.save()
