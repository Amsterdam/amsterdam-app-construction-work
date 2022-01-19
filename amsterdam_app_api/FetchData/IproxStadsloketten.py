### DEBUG IMPORT FOR DJANGO
import io
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amsterdam_app_backend.settings")
import django
django.setup()

import requests
import datetime
import threading
from amsterdam_app_api.FetchData.IproxRecursion import IproxRecursion
from amsterdam_app_api.FetchData.Image import Image
from amsterdam_app_api.GenericFunctions.Hashing import Hashing
from amsterdam_app_api.GenericFunctions.Logger import Logger
from amsterdam_app_api.GenericFunctions.TextSanitizers import TextSanitizers
from amsterdam_app_api.models import CityContact, CityOffice, CityOffices


class IproxStadsloketten:
    """ Fetch all Stadsloket details from IPROX-endpoint and convert the data into a suitable format. The format is
        described in: amsterdam_app_api.models.Stadsloket
    """
    def __init__(self):
        self.logger = Logger()
        self.url = 'https://www.amsterdam.nl/contact/?AppIdt=app-pagetype&reload=true'
        self.raw_data = dict()
        self.page = dict()
        self.sections = []
        self.stadsloketten = []

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
            self.parse_page(self.page.get('cluster', []))

    def parse_page(self, dicts):
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
                    self.sections.append({'title': title, 'html': html, 'text': text})

            # Get stadsloket locations
            if 'Verwijzing' in _dict:
                for item in _dict['Verwijzing'].get('veld', []):
                    if item.get('Nam') == 'Link':
                        title = item.get('Wrd')
                        url = item.get('link', {}).get('Url')
                        identifier = Hashing.make_md5_hash(url)
                        self.stadsloketten.append({'title': title, 'url': url, 'identifier': identifier})

        # Store contact info in db  (save method is overridden to allow only 1 single record)
        city_contact = CityContact(sections=self.sections)
        city_contact.save()
        city_offices = CityOffices(offices=self.stadsloketten)
        city_offices.save()


class IproxStadsloket:
    def __init__(self, url, identifier):
        self.logger = Logger()
        self.page = {}
        self.url = '{url}?AppIdt=app-pagetype&reload=true'.format(url=url)
        self.identifier = identifier
        self.details = {'identifier': self.identifier, 'contact': {}, 'images': {}}

        # A list for matching interesting data in retrieved json (used in the recursive_filter)
        self.page_targets = [
            'Meta',
            'Gegevens',
            'Afbeelding',
            'Blok',
            'Leestekst',
            'Lijst',
            'Omschrijving'
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
            self.parse_page(self.page.get('cluster', []))

    def parse_page(self, dicts):
        iprox = IproxRecursion()
        filtered_dicts = iprox.filter(dicts, [], targets=self.page_targets)

        # Walk through each item in filtered_dict for setting data in self.details
        for i in range(0, len(filtered_dicts), 1):
            _dict = filtered_dicts[i]

            # Info (generic) text
            if 'Gegevens' in _dict:
                for item in _dict['Gegevens']:
                    if item.get('Nam') == 'Samenvatting':
                        self.details['info'] = {
                            'html': item.get('Txt'),
                            'text': TextSanitizers.strip_html(item.get('Txt'))
                        }

            # Full text
            if 'Leestekst' in _dict:
                for item in _dict['Leestekst']:
                    if item.get('Nam') == 'Titel':
                        self.details['title'] = item.get('Wrd')
                    if item.get('Nam') == 'Tekst':
                        self.details['address'] = {
                            'html': item.get('Txt'),
                            'text': TextSanitizers.strip_html(item.get('Txt'))
                        }

            # Opening hours and contact
            if 'Omschrijving' in _dict:
                title = text = html = None
                for item in _dict['Omschrijving']:
                    if item.get('Nam') == 'Titel':
                        title = item.get('Wrd')
                    if item.get('Nam') == 'Tekst':
                        text = TextSanitizers.strip_html(item.get('Txt'))
                        html = item.get('Txt')
                if None not in (title, text, html):
                    self.details['contact'][title] = {'text': text, 'html': html}

            # Get Image(s)
            if 'Afbeelding' in _dict:
                domain = 'https://www.amsterdam.nl'
                for item in _dict['Afbeelding']:
                    if item.get('Nam') == 'Afbeelding':
                        url = "{domain}{image}".format(domain=domain, image=item.get('Src', {}).get('_'))
                        sources = {
                            'orig': {
                                "url": url,
                                "filename": item.get('FilNam'),
                                "image_id": Hashing.make_md5_hash(url),
                                "description": ""
                            }
                        }
                        assets = item.get('asset')
                        for asset in assets:
                            try:
                                url = "{domain}{image}".format(domain=domain,
                                                               image=asset.get('Src', {}).get('_'))
                                size = asset.get('Src', {}).get('_', '').split('/')[4]
                                sources[size] = {
                                    "url": url,
                                    "filename": asset.get('Src', {}).get('_', '').split('/')[-1],
                                    "image_id": Hashing.make_md5_hash(url),
                                    "description": ""
                                }
                            except Exception as error:
                                self.logger.error(error)

                        self.details['images'] = {'type': '', 'sources': sources}

        self.save()

    def save(self):
        project_details_object, created = CityOffice.objects.update_or_create(identifier=self.identifier)

        # New record
        if created is True:
            project_details_object = CityOffice(**self.details)  # Update last scrape time is done implicitly
            project_details_object.save()

        # Update existing record
        else:
            self.details['last_seen'] = datetime.datetime.now()  # Update last scrape time
            CityOffice.objects.filter(pk=self.identifier).update(**self.details)


class Scraper:
    def __init__(self):
        self.image = Image()

    def get_images(self, details):
        # Add image objects to the download queue
        for size in details['images']['sources']:
            image_object = details['images']['sources'][size]
            image_object['size'] = size
            self.image.queue.put(image_object)

    def run(self):
        # Get main stadsloket info (contact info and sub_pages urls)
        isl = IproxStadsloketten()
        isl.get_data()
        isl.parse_data()

        # scrape each stadsloket information
        for item in isl.stadsloketten:
            url = item['url']
            identifier = item['identifier']
            isl_sub = IproxStadsloket(url, identifier)
            isl_sub.get_data()
            isl_sub.parse_data()
            self.get_images(isl_sub.details)

        # Get images and IproxNews multi-threaded to speed up the scraping-process
        threads = list()

        # Fetch images (queue is filled during project scraping)
        thread_image = threading.Thread(target=self.image.run, kwargs=({'module': 'Iprox Stadsloketten'}))
        thread_image.start()
        threads.append(thread_image)

        # Join threads (blocking!)
        for thread in threads:
            thread.join()
