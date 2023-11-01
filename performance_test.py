# pylint: disable=consider-using-with
""" A simple performance test
"""
import concurrent.futures
import os
import random
import threading
import time

import requests

from construction_work.generic_functions.aes_cipher import AESCipher


class PerformanceTest:
    """Simple class to conduct a performance test"""

    def __init__(self, server=None, concurrency=None, cycles=None):
        """ """
        api = "api/v1/projects"
        fields = "followed,identifier,images,publication_date,recent_articles,subtitle,title"
        query_params = "article_max_age=60&page_size=20"
        self.url = f"http://{server}:8000/{api}?fields={fields}&{query_params}"
        self.concurrent_requests = concurrency
        self.cycles = cycles
        self.response_times = []
        self.response_sizes = []
        self.failed_requests = 0
        self.successful_requests = 0
        self.retried_requests = 0
        self.test_start = 0
        self.test_stop = 0
        self.lock = threading.Lock()

        app_token = os.getenv("APP_TOKEN")
        aes_secret = os.getenv("AES_SECRET")
        token = AESCipher(app_token, aes_secret).encrypt()
        self.headers = {"DEVICEAUTHORIZATION": token, "DEVICEID": "uwsgi+nginx+client"}

    def send_request(self, url, max_retries=5):
        """Send request to upstream server"""
        retries = 0
        start_time = time.time()

        while retries < max_retries:
            try:
                response = requests.get(url, headers=self.headers, timeout=5)  # Send GET request

                if response.status_code == 200:
                    end_time = time.time()
                    self.lock.acquire()  # Acquire the lock
                    self.response_times.append(end_time - start_time)
                    self.response_sizes.append(len(response.content))
                    self.successful_requests += 1
                    self.lock.release()  # Release the lock
                    return  # Exit the loop if the request was successful

                retries += 1
            except requests.exceptions.RequestException:
                retries += 1

            self.retried_requests += 1

        self.lock.acquire()  # Acquire the lock
        self.failed_requests += 1
        self.lock.release()  # Release the lock

    def start_test(self):
        """Perform performance testing"""
        self.test_start = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrent_requests) as executor:
            lat_lon = []
            for _ in range(self.concurrent_requests):
                lat = 52.0 + random.random()
                lon = 4 + random.random()
                lat_lon.append(f"&lat={lat}&lon={lon}")

            test_cycle = 1

            for _ in range(self.cycles):
                print(f"\rtest cycle: {test_cycle}/{self.cycles}", end="", flush=True)
                futures = []
                for i in range(self.concurrent_requests):
                    page_number = random.randint(1, 16)
                    request_url = self.url + lat_lon[i] + "&page=" + str(page_number)
                    futures.append(executor.submit(self.send_request, request_url))
                concurrent.futures.wait(futures)
                test_cycle += 1
        self.test_stop = time.time()

    def print_metrics(self):
        """Calculate statistics"""
        total_time = sum(self.response_times)
        average_time = total_time / (self.concurrent_requests * self.cycles)
        fastest_time = min(self.response_times)
        slowest_time = max(self.response_times)
        average_size = sum(self.response_sizes) / len(self.response_sizes)
        largest_size = max(self.response_sizes)
        smallest_size = min(self.response_sizes)

        # Convert sizes to kilobytes
        average_size_kb = average_size / 1024
        largest_size_kb = largest_size / 1024
        smallest_size_kb = smallest_size / 1024

        # Print the report
        print("\rPerformance Testing Report:")
        print("=" * 50)
        print(f"Concurrent requests: {self.concurrent_requests}")
        print(f"Test cycles: {self.cycles}")
        print(f"Test duration: {self.test_stop - self.test_start:.2f} s")
        print("_" * 50)
        print(
            f"Requests per second: {self.concurrent_requests * self.cycles / (self.test_stop - self.test_start):.2f}/s"
        )
        print(f"Request Time (s) (⋍, <, >): {average_time:.2f}, {fastest_time:.2f}, {slowest_time:.2f}")
        print(f"Response Size (Kb) (⋍, <, >): {average_size_kb:.2f}, {smallest_size_kb:.2f}, {largest_size_kb:.2f}")
        print("_" * 50)
        print(f"Total number of requests: {self.concurrent_requests * self.cycles}")
        print(f"Successful Requests: {self.successful_requests}")
        print(f"Failed Requests: {self.failed_requests}")
        print(f"Retried Requests: {self.retried_requests}")


if __name__ == "__main__":
    performance_test = PerformanceTest(server="0.0.0.0", concurrency=1, cycles=10)
    performance_test.start_test()
    performance_test.print_metrics()
