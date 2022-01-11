# Begin Debug
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amsterdam_app_backend.settings")
import django
django.setup()
# End debug

import requests
from amsterdam_app_api.FetchData.IproxRecursion import IproxRecursion
from amsterdam_app_api.GenericFunctions.Hashing import Hashing
from amsterdam_app_api.GenericFunctions.Logger import Logger
from amsterdam_app_api.GenericFunctions.TextSanitizers import TextSanitizers
from amsterdam_app_api.models import CityContacts


class IproxStadsloketten:
    """ Fetch all Stadsloket details from IPROX-endpoint and convert the data into a suitable format. The format is
        described in: amsterdam_app_api.models.Stadsloket
    """
    def __init__(self):
        self.logger = Logger()
        self.url = 'https://www.amsterdam.nl/contact/?AppIdt=app-pagetype&reload=true'
        self.raw_data = dict()
        self.page = dict()
        self.contact = {}
        self.stadsloketten = {}

        # A list for matching interesting data in retrieved json (used in the recursive_filter)
        self.page_targets = [
            'Meta',
            'Gegevens',
            'Samenvatting',
            'Blok',
            'Superlink',
            'Verwijzing',
            'Intern',
            'Link',
            'Lijst',
            'Omschrijving',
            'Titel',
            'Tekst',
            'Afbeelding'
        ]

    def get_data(self):
        """
        request data from IPROX-end-point

        :return: void
        """
        try:
            result = requests.get(self.url)
            self.raw_data = result.json()
            item = self.raw_data.get('item', None)
            if item is None:
                # Should not happen! It means an erroneous feed from IPROX
                return

            # Get 'blok' element (part of json with content/images/etc...)
            self.page = item.get('page', {})

            # Set page type (used to answer the question: Do we need to parse this page?)
            self.page_type = self.page.get('pagetype', '')
        except Exception as error:
            self.logger.error('failed fetching data from {url}: {error}'.format(url=self.url, error=error))

    def parse_data(self):
        # Based on page-type the data is parsed differently (e.g. news, normal page, ...)
        if self.page.get('pagetype', '') == 'subhome':
            self.parse_main_page(self.page.get('cluster', []))

    def parse_main_page(self, dicts):
        iprox = IproxRecursion()
        filtered_dicts = iprox.filter(dicts, [], targets=self.page_targets)

        # Walk through each item in filtered_dict for setting data in self.details
        for i in range(0, len(filtered_dicts), 1):
            _dict = filtered_dicts[i]

            # Set contact options
            if 'Omschrijving' in _dict:
                title = html = text = None
                for item in _dict['Omschrijving']:
                    if item.get('Nam') == 'Titel':
                        title = item.get('Wrd')
                    if item.get('Nam') == 'Tekst':
                        html = item.get('Txt')
                        text = TextSanitizers.strip_html(html)
                if None not in (title, html):
                    self.contact[title] = {'html': html, 'text': text}

            # Get stadsloket locations
            if 'Verwijzing' in _dict:
                for item in _dict['Verwijzing'].get('veld', []):
                    if item.get('Nam') == 'Link':
                        location = item.get('Wrd')
                        url = item.get('link', {}).get('Url')
                        identifier = Hashing.make_md5_hash(url)
                        self.stadsloketten[location]= {'url': url, 'identifier': identifier}

        # Store contact info in db  (save method is overridden to allow only 1 single record)
        city_contacts = CityContacts(contact=self.contact)
        city_contacts.save()


class IproxStadsloket:
    def __init__(self, url):
        self.url = '{url}'.format(url=url)


if __name__ == '__main__':
    isl = IproxStadsloketten()
    isl.get_data()
    isl.parse_data()
    pass