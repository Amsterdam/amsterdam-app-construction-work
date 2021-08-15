import requests
import threading
from queue import Queue
from amsterdam_app_api.models import Image


class ImageFetcher:
    def __init__(self):
        self.num_workers = 10
        self.queue = Queue()

    @staticmethod
    def fetch(url):
        try:
            # Request image as a stream
            result = requests.get(url, stream=True)
            if result.status_code != 200:
                raise Exception('Failed downloading image: {url}'.format(url=url))

            # start reading from the stream in chunks of 1024 bytes and append to self.data
            data = b''
            for chunk in result.iter_content(1024):
                data += chunk
            return data
        except Exception as error:
            print('failed fetching image data for {url}: {error}'.format(url=url, error=error))
            return None

    @staticmethod
    def save_image_to_db(item):
        extension = item['filename'].split('.')[-1]
        item['mime_type'] = 'image/{extension}'.format(extension=extension)
        image = Image(**item)
        image.save()

    def worker(self, worker_id):
        count = 0
        while not self.queue.empty():
            item = self.queue.get()

            # Images use identifier not image_id from other models
            item['identifier'] = item.pop('image_id')

            # Check if we already have this image in DB
            project_object, created = Image.objects.update_or_create(identifier=item.get('identifier'))
            if created is True:
                image_data = self.fetch(item['url'])
                if image_data is not None:
                    item['data'] = image_data
                    self.save_image_to_db(item)
            count += 1
        else:
            print('Worker {worker_id} out of jobs, processed {count} images. Terminating.'.format(worker_id=worker_id,
                                                                                                  count=count))

    def run(self):
        threads = list()

        # Start worker threads
        for i in range(0, self.num_workers, 1):
            thread = threading.Thread(target=self.worker, args=(i,))
            threads.append(thread)
            thread.start()

        # Stop worker threads
        for i in range(0, len(threads), 1):
            threads[i].join()
