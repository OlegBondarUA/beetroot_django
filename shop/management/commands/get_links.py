from django.core.management.base import BaseCommand, CommandError

from shop.links_scrapper import main


class Command(BaseCommand):
    help = 'Scrape data from donor.'

    def handle(self, *args, **options):
        try:
            main()
        except Exception as error:
            raise CommandError('Error happen while scrapping %s' % error)

        self.stdout.write(self.style.SUCCESS(
            'Successfully parsed data from donor.')
        )