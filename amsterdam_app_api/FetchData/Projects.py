import requests
import json
from amsterdam_app_api.GenericFunctions.Hashing import Hashing
from amsterdam_app_api.GenericFunctions.TextSanitizers import TextSanitizers
from amsterdam_app_api.models import Projects, ProjectDetails
from amsterdam_app_api.FetchData.Image import ImageFetcher


class FetchProjectDetails:
    def __init__(self, url, identifier):
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
                'coordinates': {'lon': float(), 'lat': float()},
                'timeline': {}
            },
            'district_id': -1,
            'district_name': '',
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
            'Omschrijving',
            'Samenvatting'
        ]
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
        self.details['page_id'] = int(self.page.get('PagIdt', -1))
        self.details['title'] = self.page.get('title', ''.join(self.details['rel_url'].split('/')[-1:]))

    def recursive_filter(self, data, result, targets=None, veld=None):
        # Do we need to search deeper?
        if isinstance(data, dict):
            if data.get('Nam') in targets:
                if data.get('veld', None) is not None:
                    result.append({veld: data})  # It seems this code is never reached!
                elif data.get('cluster', None) is not None:
                    result = self.recursive_filter(data['cluster'], result, targets=targets, veld=data.get('Nam'))

        elif isinstance(data, list):
            for i in range(0, len(data), 1):
                if data[i].get('Nam') in targets:
                    if data[i].get('veld', None) is not None:
                        result.append({data[i].get('Nam'): data[i].get('veld')})
                    elif data[i].get('cluster', None) is not None:
                        result = self.recursive_filter(data[i], result, targets=targets, veld=data[i].get('Nam'))

        # No! We can return the result
        return result

    def parse_page(self, dicts):
        filtered_dicts = self.recursive_filter(dicts, [], targets=self.page_targets)

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

            # Get timeline (if available)
            if filtered_dicts[i].get('Koppeling', None) is not None:
                set_timeline = False
                url = ''
                for j in range(0, len(filtered_dicts[i]['Koppeling']), 1):
                    if filtered_dicts[i]['Koppeling'][j].get('Nam', '') == 'App categorie' and filtered_dicts[i]['Koppeling'][j].get('SelAka', '') == 'when-timeline':
                        set_timeline = True
                    if filtered_dicts[i]['Koppeling'][j].get('Nam', '') == 'Link':
                        url = filtered_dicts[i]['Koppeling'][j].get('link', {}).get('Url', '')

                if set_timeline is True:
                    self.get_timeline(url)

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

    def filter_timeline(self, data):
        filtered_results = self.recursive_filter(data, [], targets=self.timeline_targets)
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
            url = 'https://www.amsterdam.nl/projecten/kademuren/maatregelen-vernieuwing/herengracht-213-243/tijdlijn-herengracht-213-243/?AppIdt=app-pagetype&reload=true'
            result = requests.get('{url}?AppIdt=app-pagetype&reload=true'.format(url=url))
            raw_data = result.json()
            clusters = raw_data.get('item', {}).get('page', {}).get('cluster', [])
            self.filter_timeline(clusters)
        except Exception as error:
            print('failed fetching timeline from data: {error}'.format(url=self.url, error=error))

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
    def __init__(self, path, project_type):
        """
        Class file to retrieve data from end-point and convert into a suitable format
        """
        self.protocol = 'https://'
        self.domain = 'www.amsterdam.nl'
        self.path = path
        self.project_type = project_type
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

        see models.Projects() for field definitions
        :return: void
        """

        for i in range(0, len(self.raw_data), 1):
            try:
                # Using md5 will yield the same result for a given string on repeated iterations, hence an identifier
                identifier = Hashing.make_md5_hash(self.raw_data[i].get('feedid', None))
                self.parsed_data.append(
                    {
                        'project_type': self.project_type,
                        'identifier': identifier,
                        'district_id': -1,  # this will be fetched on a successive call...
                        'district_name': '',  # this will be fetched on a successive call...
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


class IngestProjects:
    def __init__(self):
        self.image_fetcher = ImageFetcher()
        self.paths = {
            'brug': '/projecten/bruggen/maatregelen-vernieuwen-bruggen/',
            'kade': '/projecten/kademuren/maatregelen-vernieuwing/'
        }

        self.temp = list()

    def get_images(self, fpd_details):
        # Add image objects to the download queue
        for images in fpd_details['images']:
            for size in images['sources']:
                image_object = images['sources'][size]
                image_object['size'] = size
                self.temp.append(image_object)
                self.image_fetcher.queue.put(image_object)

    def get_set_project_details(self, item):
        fpd = FetchProjectDetails(item['source_url'], item['identifier'])
        fpd.get_data()

        # Skip news items/articles etc...
        if fpd.page_type == 'subhome':
            fpd.parse_data()
            project_details_object, created = ProjectDetails.objects.update_or_create(identifier=item.get('identifier'))

            # New record
            if created is True:
                project_details_object = ProjectDetails(**fpd.details)
                project_details_object.save()

            # Update existing record
            else:
                ProjectDetails.objects.filter(pk=item.get('identifier')).update(**fpd.details)

            # Add images from this project to the download queue
            self.get_images(fpd.details)
            return fpd.details
        return None

    def get_set_projects(self, project_type):
        path = self.paths[project_type]
        # Fetch projects and ingest data
        fpa = FetchProjectAll(path, project_type)
        fpa.get_data()
        fpa.parse_data()

        updated = new = unmodified = failed = 0
        for item in fpa.parsed_data:
            try:
                project_object, created = Projects.objects.update_or_create(identifier=item.get('identifier'))

                # New record
                if created is True:
                    result = self.get_set_project_details(item)
                    if result is not None:
                        item['images'] = result['images']
                        item['district_id'] = result['district_id']
                        item['district_name'] = result['district_name']
                        project_object = Projects(**item)
                        project_object.save()
                        new += 1
                    else:
                        Projects.objects.get(pk=item.get('identifier')).delete()

                # Update existing record
                else:
                    if item.get('modification_date', None) != project_object.modification_date:
                        result = self.get_set_project_details(item)
                        if result is not None:
                            item['images'] = result['images']
                            item['district_id'] = result['district_id']
                            item['district_name'] = result['district_name']
                            Projects.objects.filter(pk=item.get('identifier')).update(**item)
                            updated += 1
                        else:
                            Projects.objects.get(pk=item.get('identifier')).delete()
                    else:
                        unmodified += 1

            except Exception as error:
                print('failed ingesting data {project}: {error}'.format(project=item.get('title'), error=error))
                failed += 1

        # Fetch images (queue is filled during project scraping)
        self.image_fetcher.run()
        return {'new': new, 'updated': updated, 'unmodified': unmodified, 'failed': failed}


if __name__ == '__main__':
    fpd = FetchProjectDetails('','')
    fpd.get_timeline('')