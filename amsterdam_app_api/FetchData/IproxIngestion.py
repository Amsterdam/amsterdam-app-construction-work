import threading
import datetime
from amsterdam_app_api.models import Projects, ProjectDetails
from amsterdam_app_api.FetchData.Image import Image
from amsterdam_app_api.GenericFunctions.Logger import Logger
from amsterdam_app_api.FetchData.IproxProject import IproxProject
from amsterdam_app_api.FetchData.IproxProjects import IproxProjects
from amsterdam_app_api.FetchData.IproxGarbageCollector import IproxGarbageCollector
from amsterdam_app_api.FetchData.IproxNews import IproxNews


class IproxIngestion:
    """ Ingest projects will call the IPROX-endpoint based on path (url). It will fetch the data in three stages:

        stage 1: Fetch all projects based on path
        stage 2: Fetch all project details based on result from stage 1
        stage 3: Fetch all images based on result from stage 2

        Ingest Projects will skip fetching records based on modification time. (eg. only fetch new records)

        Garbage collecting:

        The garbage collector is initialized with current time. All projects with a last_seen time before current time
        are possibly due for garbage collecting. See details in class IproxGarbageCollector.
    """

    def __init__(self):
        self.logger = Logger()
        self.iprox_garbage_collector = IproxGarbageCollector(last_scrape_time=datetime.datetime.now())
        self.image = Image()
        self.news = IproxNews()
        self.paths = {
            'brug': '/projecten/bruggen/maatregelen-vernieuwen-bruggen/',
            'kade': '/projecten/kademuren/maatregelen-vernieuwing/'
        }

    def get_images(self, fpd_details):
        # Add image objects to the download queue
        for images in fpd_details['images']:
            for size in images['sources']:
                image_object = images['sources'][size]
                image_object['size'] = size
                self.image.queue.put(image_object)

    def queue_news(self, fpd_details):
        # add news_items to the IproxNews.queue for scraping
        for news_item in fpd_details['news']:
            self.news.queue.put({'news_item': news_item, 'project_type': fpd_details['project_type']})

    def get_set_project_details(self, item, project_type):
        fpd = IproxProject(item['source_url'], item['identifier'])
        fpd.get_data()

        # Skip news items/articles etc...
        if fpd.page_type == 'subhome':
            fpd.parse_data()
            fpd.details['project_type'] = project_type
            project_details_object, created = ProjectDetails.objects.update_or_create(identifier=item.get('identifier'))

            # New record
            if created is True:
                project_details_object = ProjectDetails(**fpd.details)  # Update last scrape time is done implicitly
                project_details_object.save()

            # Update existing record
            else:
                fpd.details['last_seen'] = datetime.datetime.now()  # Update last scrape time
                ProjectDetails.objects.filter(pk=item.get('identifier')).update(**fpd.details)

            # Add images from this project to the download queue
            self.get_images(fpd.details)

            # Add news items from this project to the IproxNews.queue() for fetching
            self.queue_news(fpd.details)

            return fpd.details
        return None

    def get_set_projects(self, project_type):
        # Set the url path from where to fetch the projects
        path = self.paths[project_type]

        # Fetch projects and ingest data
        fpa = IproxProjects(path, project_type)
        fpa.get_data()
        fpa.parse_data()

        updated = new = failed = 0
        for item in fpa.parsed_data:
            try:
                project_object, created = Projects.objects.update_or_create(identifier=item.get('identifier'))

                # New record
                if created is True:
                    result = self.get_set_project_details(item, project_type)
                    if result is not None:
                        item['images'] = result['images']
                        item['district_id'] = result['district_id']
                        item['district_name'] = result['district_name']
                        project_object = Projects(**item)
                        project_object.save()  # Update last scrape time is done implicitly
                        new += 1
                    else:
                        Projects.objects.get(pk=item.get('identifier')).delete()

                # Update existing record
                else:
                    result = self.get_set_project_details(item, project_type)
                    if result is not None:
                        item['images'] = result['images']
                        item['district_id'] = result['district_id']
                        item['district_name'] = result['district_name']
                        item['last_seen'] = datetime.datetime.now()  # Update last scrape time
                        Projects.objects.filter(pk=item.get('identifier')).update(**item)
                        updated += 1
                    else:
                        Projects.objects.get(pk=item.get('identifier')).delete()

            except Exception as error:
                self.logger.error('failed ingesting data {project}: {error}'.format(project=item.get('title'), error=error))
                failed += 1

        # Get images and IproxNews multi-threaded to speed up the scraping-process
        threads = list()

        # Fetch news
        thread_news = threading.Thread(target=self.news.run)
        thread_news.start()
        threads.append(thread_news)

        # Fetch images (queue is filled during project scraping)
        thread_image = threading.Thread(target=self.image.run, kwargs=({'module': 'Iprox Project Details'}))
        thread_image.start()
        threads.append(thread_image)

        # Join threads (blocking!)
        for thread in threads:
            thread.join()

        self.iprox_garbage_collector.run(project_type=project_type)
        return {'new': new, 'updated': updated, 'failed': failed}
