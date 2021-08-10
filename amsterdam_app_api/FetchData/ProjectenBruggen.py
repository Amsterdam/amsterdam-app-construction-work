import requests
import json
from amsterdam_app_api.GenericFunctions.Hashing import Hashing
from amsterdam_app_api.GenericFunctions.TextSanitizers import TextSanitizers


class FetchProjectDetails:
    def __init__(self, url):
        self.url = '{url}?AppIdt=app-pagetype&reload=true'.format(url=url)
        self.raw_data = dict()
        self.page = dict()
        self.page_type = ''

        # Data model
        self.details = {
            'body': {
                'contact': [],  # [{'text': '', 'html': '', 'title': ''}, ...],
                'what': [],  # [{'text': '', 'html': '', 'title': ''}, ...],
                'when': [],  # [{'text': '', 'html': '', 'title': ''}, ...],
                'where': [],  # [{'text': '', 'html': '', 'title': ''}, ...],
                'work': [],  # [{'text': '', 'html': '', 'title': ''}, ...],
                'more-info': [],  # [{'text': '', 'html': '', 'title': ''}, ...],
                'coordinates': {'lon': None, 'lat': None}
            },
            'districts_id': -1,
            'dictricts_name': '',
            'images': [
                # {
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
            'page_id': -1,
            'title': '',
            'rel_url': '',
            'url': ''
        }

        # A list for matching interesting data in retrieved json
        self.targets = [
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
            'Lijst',
            'Meta',
            'Omschrijving',
            'Samenvatting'
        ]

    def get_data(self):
        """
        request data from data-end point

        :return: void
        """
        try:
            result = requests.get(self.url)
            self.raw_data = result.json()
            item = self.raw_data.get('item', None)
            if item is None:
                # Should not happen!
                return

            # Get blok element (part of json with content/images/etc...)
            self.page = item.get('page', {})

            # Set page type (used to answer the question: Do we need to parse this page?)
            self.page_type = self.page.get('pagetype', '')
        except Exception as error:
            print('failed fetching data from {url}: {error}'.format(url=self.url, error=error))

    def parse_data(self):
        # Based on pagetype the data is parsed differently (e.g. news, normal page, ...)
        if self.page.get('pagetype', '') == 'subhome':
            self.parse_page(self.page.get('cluster', []))

        elif self.page.get('pagetype', '') == 'nieuwsartikel':
            return

        # Get/Set url, rel_url
        self.details['url'] = self.raw_data.get('item').get('Url', self.url)
        self.details['rel_url'] = self.raw_data.get('item').get('relUrl', '/'.join(self.url.split('/')[3:-1]))

        # Set page identifier and title
        self.details['page_id'] = self.page.get('PagIdt', -1)
        self.details['title'] = self.page.get('title', ''.join(self.details['rel_url'].split('/')[-1:]))

    def recursive_filter(self, data, result, veld=None):
        # Do we need to search deeper?
        if isinstance(data, dict):
            if data.get('Nam') in self.targets:
                if data.get('veld', None) is not None:
                    result.append({veld: data})  # It seems this code is never reached!
                elif data.get('cluster', None) is not None:
                    result = self.recursive_filter(data['cluster'], result, veld=data.get('Nam'))

        elif isinstance(data, list):
            for i in range(0, len(data), 1):
                if data[i].get('Nam') in self.targets:
                    if data[i].get('veld', None) is not None:
                        result.append({data[i].get('Nam'): data[i].get('veld')})
                    elif data[i].get('cluster', None) is not None:
                        result = self.recursive_filter(data[i], result, veld=data[i].get('Nam'))

        # No! We can return the result
        return result

    def parse_page(self, dicts):
        filtered_dicts = self.recursive_filter(dicts, [])

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

                if app_category is not None:
                    self.set_text_result(result, app_category)

            # Set Coordinates (if available).
            # Note: EPSG:4326 is an identifier of WGS84. WGS84 comprises a standard coordinate frame for the Earth
            if filtered_dicts[i].get('Coordinaten', None) is not None:
                self.set_geo_data(filtered_dicts[i]['Coordinaten']['Txt']['geo']['json'])

            if filtered_dicts[i].get('Kenmerken', None) is not None and filtered_dicts[i].get('Kenmerken').get('Src') == 'Stadsdeel':
                self.details['districts_id'] = filtered_dicts[i].get('Kenmerken').get('SelItmIdt')
                self.details['dictricts_name'] = filtered_dicts[i].get('Kenmerken').get('Wrd')

    def set_text_result(self, data, app_category):
        if data['html'] != '':
            if app_category in self.details['body']:
                self.details['body'][app_category].append(data)
            else:
                self.details['body'][app_category] = [data]

    def set_geo_data(self, json_data):
        try:
            geo_data = [x for x in json_data if x['type'] == 'EPSG:4326'][0]
            data = json.loads(geo_data['_'])
            coordinates = data['features'][0]['geometry']['coordinates']
            self.details['body']['coordinates'] = {'lon': float(coordinates[0]), 'lat': float(coordinates[1])}
        except Exception as error:
            print('failed fetching coordinates from data: {error}'.format(url=self.url, error=error))

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


class FetchProjectAll:
    def __init__(self, path=None):
        """
        Class file to retrieve data from end-point and convert into a suitable format
        """
        self.protocol = 'https://'
        self.domain = 'www.amsterdam.nl'
        self.path = path
        self.query_params = '?new_json=true&pager_rows=1000'
        self.url = '{protocol}{domain}{path}{query_params}'.format(protocol=self.protocol,
                                                                   domain=self.domain,
                                                                   path=self.path,
                                                                   query_params=self.query_params)
        self.raw_data = list()
        self.parsed_data = list()

    def get_data(self):
        """
        request data from data-end point

        :return: void
        """
        try:
            result = requests.get(self.url)
            self.raw_data = result.json()
        except Exception as error:
            print('failed fetching data from {url}: {error}'.format(url=self.url, error=error))

    def parse_data(self):
        """
        Convert data from end-point

        districts_id = integer
        title = string
        content_html = string
        content_text = string
        images = list
        identifier = string
        publication_data = string
        modification_data = string
        source_url = string
        :return: void
        """

        for i in range(0, len(self.raw_data), 1):
            try:
                # Using md5 will yield the same result for a given string on repeated iterations, hence an identifier
                identifier = Hashing.make_md5_hash(self.raw_data[i].get('feedid', None))
                # identifier = hashlib.md5(self.raw_data[i].get('feedid', None).encode()).hexdigest()
                self.parsed_data.append(
                    {
                        'identifier': identifier,
                        'districts_id': -1,  # this will be fetched on a successive call...
                        'title': self.raw_data[i].get('title', ''),
                        'content_html': self.raw_data[i].get('content', ''),
                        'content_text': TextSanitizers.strip_html(self.raw_data[i].get('content', '')),
                        'images': [],  # these will be fetched on a successive call...
                        'publication_date': self.raw_data[i].get('publication_date', ''),
                        'modification_date': self.raw_data[i].get('modification_date', ''),
                        'source_url': self.raw_data[i].get('source_url', '')
                    }
                )
            except Exception as error:
                print('failed parsing data from {url}: {error}'.format(url=self.url, error=error))


if __name__ == '__main__':
    import time
    now = time.time()
    paths = [
        '/projecten/bruggen/maatregelen-vernieuwen-bruggen/',
        '/projecten/kademuren/maatregelen-vernieuwing/'
    ]
    for path in paths:
        fpa = FetchProjectAll(path=path)
        fpa.get_data()
        fpa.parse_data()

        data = list()
        # for i in [8]:
        for i in range(0, len(fpa.parsed_data), 1):
            fpd = FetchProjectDetails(fpa.parsed_data[i]['source_url'])
            fpd.get_data()
            if fpd.page_type == 'subhome':
                fpd.parse_data()
                fpa.parsed_data[i]['images'] = fpd.details['images']
                data.append(fpd.details)
            else:
                print('{title} <-> {page_type}'.format(title=fpa.parsed_data[i]['title'], page_type=fpd.page_type))

        print('Done fetching: {path}'.format(path=path))

    print(time.time() - now)
