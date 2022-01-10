import json
import requests
from amsterdam_app_api.FetchData.IproxRecursion import IproxRecursion
from amsterdam_app_api.GenericFunctions.Hashing import Hashing
from amsterdam_app_api.GenericFunctions.Logger import Logger
from amsterdam_app_api.GenericFunctions.TextSanitizers import TextSanitizers


class IproxProject:
    """ Fetch all project details from IPROX-endpoint and convert the data into a suitable format. The format is
        described in: amsterdam_app_api.models.Projects
    """
    def __init__(self, url, identifier):
        self.logger = Logger()
        self.identifier = identifier
        self.url = '{url}?AppIdt=app-pagetype&reload=true'.format(url=url)
        self.raw_data = dict()
        self.page = dict()
        self.page_type = ''

        # Data model
        self.details = {
            'identifier': identifier,
            'body': {
                'contact': [],  # [{'text': '', 'html': '', 'title': ''}, ...],
                'what': [],  # [{'text': '', 'html': '', 'title': ''}, ...],
                'when': [],  # [{'text': '', 'html': '', 'title': ''}, ...],
                'where': [],  # [{'text': '', 'html': '', 'title': ''}, ...],
                'work': [],  # [{'text': '', 'html': '', 'title': ''}, ...],
                'more-info': [],  # [{'text': '', 'html': '', 'title': ''}, ...],
                'timeline': {}
            },
            'coordinates': {'lon': float(), 'lat': float()},
            'district_id': -1,
            'district_name': '',
            'images': [
                # { EXAMPLE:
                #     'type': '',
                #     'sources': {
                #         'orig': {'url': '', 'image_id': '', 'filename': '', 'description': ''},
                #         '80px': {'url': '', 'image_id': '', 'filename': '', 'description': ''},
                #         '220px': {'url': '', 'image_id': '', 'filename': '', 'description': ''},
                #         '460px': {'url': '', 'image_id': '', 'filename': '', 'description': ''},
                #         '700px': {'url': '', 'image_id': '', 'filename': '', 'description': ''}
                #     }
                # }
            ],
            'news': [
                # { EXAMPLE:
                #     'project_identifier': self.identifier,
                #     'identifier': '',
                #     'url': ''
                # }
            ],
            'page_id': -1,
            'title': '',  # If a title has a ':' title is the part before ':' else '~full title'
            'subtitle': '',  # If a title has a ':' subtitle is the part after ':' else ''
            'rel_url': '',
            'url': ''
        }

        # A list for matching interesting data in retrieved json (used in the recursive_filter)
        self.page_targets = [
            'Afbeelding',
            'Afbeeldingen',
            'App categorie'
            'Auteur',
            'Basis afbeelding',
            'Blok',
            'Brondatum',
            'Coordinaten',
            'Fotoshow',
            'Gegevens',
            'Inhoud',
            'Kenmerk',
            'Kenmerken',
            'Koppeling',
            'Lijst',
            'Meta',
            'Nieuws',
            'Omschrijving',
            'Samenvatting'
        ]

        # A list for matching interesting data in retrieved json (used in the recursive_filter)
        self.timeline_targets = [
            'Meta',
            'Gegevens',
            'Inhoud',
            'Eigenschappen',
            'Instellingen',
            'Tijdlijn',
            'Hoofditem'
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

        # Not implemented yet.
        elif self.page.get('pagetype', '') == 'nieuwsartikel':
            return

        # Get/Set url, rel_url
        self.details['url'] = self.raw_data.get('item').get('Url', self.url)
        self.details['rel_url'] = self.raw_data.get('item').get('relUrl', '/'.join(self.url.split('/')[3:-1]))

        # Set page identifier and title
        self.details['page_id'] = int(self.page.get('PagIdt', -1))
        title = self.page.get('title', '').split(':')
        subtitle = None if len(title) == 1 else TextSanitizers.sentence_case("".join([title[i] for i in range(1, len(title))]))
        self.details['title'] = title[0]
        self.details['subtitle'] = subtitle

    def parse_page(self, dicts):
        iprox = IproxRecursion()
        filtered_dicts = iprox.filter(dicts, [], targets=self.page_targets)

        # Walk through each item in filtered_dict for setting data in self.details
        for i in range(0, len(filtered_dicts), 1):
            # Set images
            if filtered_dicts[i].get('Afbeelding', None) is not None:
                self.details['images'] += self.set_images(filtered_dicts[i])

            # Set text items
            if filtered_dicts[i].get('Omschrijving', None) is not None:
                result = {'title': '', 'html': '', 'text': ''}
                app_category = None
                for j in range(0, len(filtered_dicts[i]['Omschrijving']), 1):
                    # Get App category
                    if filtered_dicts[i]['Omschrijving'][j].get('Nam', '') == 'App categorie':
                        app_category = filtered_dicts[i]['Omschrijving'][j].get('SelAka', None)

                    # Get Title
                    if filtered_dicts[i]['Omschrijving'][j].get('Nam', '') == 'Titel':
                        result['title'] = filtered_dicts[i]['Omschrijving'][j].get('Wrd', '')

                    # Get Text
                    if filtered_dicts[i]['Omschrijving'][j].get('Nam', '') == 'Tekst':
                        result['html'] = filtered_dicts[i]['Omschrijving'][j].get('Txt', '')
                        result['text'] = TextSanitizers.strip_html(filtered_dicts[i]['Omschrijving'][j].get('Txt', ''))

                # Only set text items is there is an app_category (eg. omit bogus items!)
                if app_category is not None:
                    self.set_text_result(result, app_category)

            # Get timeline (if available)
            if filtered_dicts[i].get('Koppeling', None) is not None:
                set_timeline = False
                set_news = False
                url = ''
                for j in range(0, len(filtered_dicts[i]['Koppeling']), 1):
                    if filtered_dicts[i]['Koppeling'][j].get('Nam', '') == 'App categorie':
                        if filtered_dicts[i]['Koppeling'][j].get('SelAka', '') == 'when-timeline':
                            set_timeline = True
                        elif filtered_dicts[i]['Koppeling'][j].get('SelAka', '') == 'news':
                            set_news = True
                    if filtered_dicts[i]['Koppeling'][j].get('Nam', '') == 'Link':
                        url = filtered_dicts[i]['Koppeling'][j].get('link', {}).get('Url', '')

                if set_timeline is True and url != '':
                    self.get_timeline(url)
                elif set_news is True and url != '':
                    self.get_news_items(url)

            # Set Coordinates (if available).
            # Note: EPSG:4326 is an identifier of WGS84. WGS84 comprises a standard coordinate frame for the Earth
            if filtered_dicts[i].get('Coordinaten', None) is not None:
                self.set_geo_data(filtered_dicts[i]['Coordinaten']['Txt']['geo']['json'])

            # Get district name and identifier
            if filtered_dicts[i].get('Kenmerken', None) is not None and filtered_dicts[i].get('Kenmerken').get('Src') == 'Stadsdeel':
                self.details['district_id'] = int(filtered_dicts[i].get('Kenmerken').get('SelItmIdt'))
                self.details['district_name'] = filtered_dicts[i].get('Kenmerken').get('Wrd')

    def set_text_result(self, data, app_category):
        if data['html'] != '':
            if app_category in self.details['body']:
                self.details['body'][app_category].append(data)
            else:
                self.details['body'][app_category] = [data]

    """ TIMELINE-BEGIN """

    def filter_timeline(self, data):
        iprox = IproxRecursion()
        filtered_results = iprox.filter(data, [], targets=self.timeline_targets)

        timeline_items = list()
        gegevens = dict()
        inhoud = dict()

        for i in range(0, len(filtered_results), 1):
            if filtered_results[i].get('Gegevens', None) is not None:
                gegevens = filtered_results[i].get('Gegevens', {})
            if filtered_results[i].get('Inhoud', None) is not None:
                inhoud = filtered_results[i].get('Inhoud', {})

        for i in range(0, len(filtered_results), 1):
            if filtered_results[i].get('Eigenschappen', None):
                timeline_items.append({'Eigenschappen': filtered_results[i].get('Eigenschappen'),
                                 'Instellingen': filtered_results[i + 1].get('Instellingen')})
        self.set_timeline(gegevens, inhoud, timeline_items)

    def set_timeline(self, gegevens, inhoud, timeline_items):
        timeline = {
            'title': {
                'text': TextSanitizers.strip_html(gegevens.get('Txt')),
                'html': gegevens.get('Txt')
            },
            'intro': {
                'text': TextSanitizers.strip_html(inhoud.get('Txt')),
                'html': inhoud.get('Txt')
            },
            'items': []
        }
        for timeline_item in timeline_items:
            item = {}
            for eigenschap in timeline_item.get('Eigenschappen', []):
                if eigenschap.get('Nam', None) == 'Titel':
                    item['title'] = {
                        'text': TextSanitizers.strip_html(eigenschap.get('Wrd')),
                        'html': eigenschap.get('Wrd')
                    }
                elif eigenschap.get('Nam', None) == 'Inleiding':
                    item['content'] = {
                        'text': TextSanitizers.strip_html(eigenschap.get('Txt')),
                        'html': eigenschap.get('Txt')
                    }

            for instelling in timeline_item.get('Instellingen', []):
                if instelling.get('Nam', None) == 'Status':
                    item['progress'] = instelling.get('SelWrd', '')
                if instelling.get('Nam', None) == 'Subitems initieel ingeklapt':
                    item['collapsed'] = bool(int(instelling.get('Wrd')))
            timeline['items'].append(item)
        self.details['body']['timeline'] = timeline

    def get_timeline(self, url):
        try:
            result = requests.get('{url}?AppIdt=app-pagetype&reload=true'.format(url=url))
            raw_data = result.json()
            clusters = raw_data.get('item', {}).get('page', {}).get('cluster', [])
            self.filter_timeline(clusters)
        except Exception as error:
            self.logger.error('failed fetching timeline from data: {error}'.format(url=self.url, error=error))

    """ TIMELINE-END """

    """ NEWS-BEGIN """

    def set_news_item(self, data):
        item = {
            'identifier': Hashing.make_md5_hash(data.get('feedid')),
            'project_identifier': self.identifier,
            'url': data.get('feedid')
        }
        self.details['news'].append(item)

    def get_news_items(self, url):
        try:
            self.logger.info('Found news item: {url}?new_json=true'.format(url=url))
            result = requests.get('{url}?new_json=true'.format(url=url))
            raw_data = result.json()
            if isinstance(raw_data, list) and len(raw_data) > 0:
                for i in range(0, len(raw_data), 1):
                    self.set_news_item(raw_data[i])
        except Exception as error:
            self.logger.error('failed fetching news from data: {error}'.format(url=self.url, error=error))

    """ NEWS-END """

    def set_geo_data(self, json_data):
        try:
            geo_data = [x for x in json_data if x['type'] == 'EPSG:4326'][0]
            data = json.loads(geo_data['_'])
            coordinates = data['features'][0]['geometry']['coordinates']
            self.details['coordinates'] = {'lon': float(coordinates[0]), 'lat': float(coordinates[1])}
        except Exception as error:
            self.logger.error('failed fetching coordinates from data: {error}'.format(url=self.url, error=error))

    @staticmethod
    def set_images(dicts):
        domain = 'https://www.amsterdam.nl'
        all_images = list()
        images = dict()

        # If we're dealing with a list of 'Afbeeldingen'
        if isinstance(dicts.get('Afbeelding'), list):
            for i in range(0, len(dicts.get('Afbeelding', [])), 1):
                # If the 'Nam' equals 'Afbeeldingen' there are most likely actual images embedded.
                if dicts['Afbeelding'][i].get('Nam', '') == 'Afbeelding':
                    for image in dicts['Afbeelding'][i].get('asset', {}):
                        url = ''.join([domain, image.get('Src', {}).get('_', '')])
                        key = image.get('Src').get('_').split('/')[-2]
                        images[key] = {
                            'url': url,
                            'image_id': Hashing.make_md5_hash(url),
                            'filename': image.get('FilNam', ''),
                            'description': ''
                        }

                    images['orig'] = {
                        'url': ''.join([domain, dicts['Afbeelding'][i].get('Src', {}).get('_', '')]),
                        'image_id': Hashing.make_md5_hash(''.join([domain, dicts['Afbeelding'][i].get('Src', {}).get('_', '')])),
                        'filename': dicts['Afbeelding'][i].get('FilNam', ''),
                        'description': ''
                    }
                    all_images.append({'type': '', 'sources': images})

        # If we're dealing with a dict of 'Afbeeldingen'
        if isinstance(dicts.get('Afbeelding'), dict):
            for image in dicts['Afbeelding'].get('asset', {}):
                url = ''.join([domain, image.get('Src', {}).get('_', '')])
                key = image.get('Src').get('_').split('/')[-2]
                images[key] = {
                    'url': url,
                    'image_id': Hashing.make_md5_hash(url),
                    'filename': image.get('FilNam', ''),
                    'description': ''
                }
            images['orig'] = {
                'url': ''.join([domain, dicts['Afbeelding'].get('Src', {}).get('_', '')]),
                'image_id': Hashing.make_md5_hash(''.join([domain, dicts['Afbeelding'].get('Src', {}).get('_', '')])),
                'filename': dicts['Afbeelding'].get('FilNam', ''),
                'description': ''
            }
            all_images.append({'type': '', 'sources': images})

        return all_images

