""" unit_tests """
import base64
import os

from django.test import Client, TestCase

from construction_work.api_messages import Messages
from construction_work.generic_functions.aes_cipher import AESCipher
from construction_work.models import Image

messages = Messages()


class TestApiImage(TestCase):
    """Test image"""

    def setUp(self):
        """Setup test db"""
        self.api_url = "/api/v1/image"
        self.client = Client()

        app_token = os.getenv("APP_TOKEN")
        aes_secret = os.getenv("AES_SECRET")
        token = AESCipher(app_token, aes_secret).encrypt()
        self.headers = {"DeviceAuthorization": token}

    def tearDown(self) -> None:
        Image.objects.all().delete()

    def test_get_image(self):
        """Test get image"""
        base64_small_green_square = "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAIAAAACUFjqAAAAE0lEQVR4nGNkaGDAA5jwSY5caQCnUgCUBZU3vQAAAABJRU5ErkJggg=="  # pylint: disable=line-too-long
        binary_data = base64.b64decode(base64_small_green_square)

        image = Image(
            data=binary_data,
            description="foobar",
            width=10,
            height=10,
            aspect_ratio=1,
            coordinates=None,
            mime_type="image/png",
        )
        image.save()

        response = self.client.get(self.api_url, {"id": image.pk}, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, binary_data)

        base64_data = base64.b64encode(binary_data).decode("utf-8")
        self.assertEqual(base64_data, base64_small_green_square)

    def test_no_image_id(self):
        """Test without passing image id"""
        response = self.client.get(self.api_url, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_image_does_exist(self):
        """Test request image that does not exist"""
        response = self.client.get(self.api_url, {"id": 9999}, headers=self.headers)
        self.assertEqual(response.status_code, 404)
