from django.core.management.base import BaseCommand, CommandError
from scrapers.views import techvibes, stackoverflow, marsdd

class Command(BaseCommand):
    help = 'Runs all the job scrapers and populates the database with the results'

    def handle(self, *args, **options):
        techvibes()
        stackoverflow()
        marsdd()
        self.stdout.write(self.style.SUCCESS('Success!'))
