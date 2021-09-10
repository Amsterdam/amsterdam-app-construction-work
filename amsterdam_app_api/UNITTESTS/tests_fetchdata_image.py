from django.test import TestCase
from unittest.mock import patch
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.UNITTESTS.mock_functions import mocked_requests_get
from amsterdam_app_api.UNITTESTS.mock_functions import MockedThreading
from amsterdam_app_api.FetchData.Image import Image as ImageFetcher
from amsterdam_app_api.models import Image as ImageModel
from amsterdam_app_api.serializers import ImageSerializer


class TestImages(TestCase):
    @patch('requests.get', side_effect=mocked_requests_get)
    @patch('threading.Thread', side_effect=MockedThreading)
    def test_fetch_image(self, mocked_requests_get, MockedThreading):
        image_fetcher = ImageFetcher()
        data = TestData()
        for job in data.image_download_jobs:
            image_fetcher.queue.put(job)
        image_fetcher.run()

        image_objects = ImageModel.objects.all()
        serializer = ImageSerializer(image_objects, many=True)

        self.assertEqual(len(serializer.data), 1)
