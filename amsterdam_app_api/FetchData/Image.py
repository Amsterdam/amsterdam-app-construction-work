import requests
import threading
import base64
from queue import Queue
# from amsterdam_app_api.models import Image


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
        path = ''.join(['/Users/robert/programming/Adam/Amsterdam-App-Backend/Images/',
                        item['identifier'],
                        item['extension']])
        with open(path, 'wb') as f:
            f.write(item['data'])

    def worker(self, worker_id):
        while not self.queue.empty():
            item = self.queue.get()
            image_data = self.fetch(item['url'])
            if image_data is not None:
                item['data'] = image_data
                self.save_image_to_db(item)
        else:
            print('Worker {worker_id} out of jobs, terminating.'.format(worker_id=worker_id))

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


if __name__ == '__main__':
    item = {
        'identifier': 'test',
        'extension': '.jpg',
        'url': 'https://www.amsterdam.nl/publish/pages/946448/940x415_lijnbaansgracht_-_brug_110.jpg'
    }
    image_fetcher = ImageFetcher()
    image_fetcher.queue.put(item)
    image_fetcher.run()
