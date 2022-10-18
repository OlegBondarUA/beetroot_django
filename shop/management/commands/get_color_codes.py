import re

from django.core.management.base import BaseCommand, CommandError
import requests
from bs4 import BeautifulSoup

from shop.models import Color


class Command(BaseCommand):
    help = 'Scrape color hex data.'
    url = 'https://www.color-hex.com/color-names.html'

    def handle(self, *args, **options):
        try:
            with requests.Session() as session:
                response = session.get(self.url)
                assert response.status_code == 200
            soup = BeautifulSoup(response.text, 'html.parser')
            colors = soup.select('table tbody tr td')
            colors_dict = {}
            for i in range(0, len(colors) - 2, 3):
                colors_dict[colors[i].text.strip().lower()] = colors[i + 2].text.strip()

            colors_list = []
            all_colors = Color.objects.filter(hex_code='')
            for color in all_colors:
                names = color.name.split()
                for name in names:
                    filtered_values = list(filter(lambda v: re.match(f'{name}', v), colors_dict.keys()))

                    if filtered_values:
                        color.hex_code = colors_dict[filtered_values[0]]
                        colors_list.append(color)

            Color.objects.bulk_update(colors_list, ['hex_code'])

        except Exception as error:
            raise CommandError('Error happen while scrapping %s' % error)

        self.stdout.write(self.style.SUCCESS(
            'Successfully parsed data from donor.')
        )
