from django.core.management.base import BaseCommand, CommandError
from scrapers.views import techvibes

class Command(BaseCommand):
    help = 'Runs all the job scrapers and populates the database with the results'

    def handle(self, *args, **options):
        techvibes()
        self.stdout.write(self.style.SUCCESS('Success!'))
