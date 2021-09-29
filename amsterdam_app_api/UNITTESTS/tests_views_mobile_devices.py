from django.test import Client
from django.test import TestCase
from amsterdam_app_api.GenericFunctions.AESCipher import AESCipher
from amsterdam_app_api.models import MobileDevices
from amsterdam_app_api.serializers import MobileDevicesSerializer
from amsterdam_app_api.api_messages import Messages

messages = Messages()


class TestApiDeviceRegistration(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestApiDeviceRegistration, self).__init__(*args, **kwargs)
        self.url = '/api/v1/device_registration'
        self.token = AESCipher('44755871-9ea6-4018-b1df-e4f00466c723', '6886b31dfe27e9306c3d2b553345d9e5').encrypt()

    def setUp(self):
        MobileDevices.objects.all().delete()

    def test_register_device_valid(self):
        json_data = '{"identifier": "0000000000", "os_type": "ios", "projects": ["0000000000"]}'

        c = Client()
        result = c.post(self.url, json_data, headers={"DeviceAuthorization": self.token}, content_type="application/json")

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': 'Device registration updated'})

    def test_register_device_update(self):
        c = Client()

        json_data0 = '{"identifier": "0000000000", "os_type": "ios", "projects": ["0000000000"]}'
        result = c.post(self.url, json_data0, headers={"DeviceAuthorization": self.token}, content_type="application/json")

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': 'Device registration updated'})

        json_data1 = '{"identifier": "0000000000", "os_type": "ios", "projects": ["0000000000", "1111111111"]}'
        result = c.post(self.url, json_data1, headers={"DeviceAuthorization": self.token}, content_type="application/json")

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': 'Device registration updated'})

        mobile_devices = MobileDevices.objects.all()
        serializer = MobileDevicesSerializer(mobile_devices, many=True)
        self.assertEqual(len(serializer.data), 1)

    def test_register_device_auto_removal(self):
        c = Client()

        json_data0 = '{"identifier": "0000000000", "os_type": "ios", "projects": ["0000000000"]}'
        result = c.post(self.url, json_data0, headers={"DeviceAuthorization": self.token}, content_type="application/json")

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': 'Device registration updated'})

        json_data1 = '{"identifier": "0000000000", "os_type": "ios", "projects": []}'
        result = c.post(self.url, json_data1, headers={"DeviceAuthorization": self.token}, content_type="application/json")

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': 'Device registration updated'})

        mobile_devices = MobileDevices.objects.all()
        serializer = MobileDevicesSerializer(mobile_devices, many=True)
        self.assertEqual(len(serializer.data), 0)

    def test_register_device_invalid_request(self):
        c = Client()

        json_data0 = '{"identifier": "0000000000", "projects": ["0000000000"]}'
        result = c.post(self.url, json_data0, headers={"DeviceAuthorization": self.token}, content_type="application/json")

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

        json_data1 = '{"os_type": "ios", "projects": ["0000000000"]}'
        result = c.post(self.url, json_data1, headers={"DeviceAuthorization": self.token}, content_type="application/json")

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_register_device_delete(self):
        c = Client()

        json_data0 = '{"identifier": "0000000000", "os_type": "ios", "projects": ["0000000000"]}'
        result = c.post(self.url, json_data0, headers={"DeviceAuthorization": self.token}, content_type="application/json")

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': 'Device registration updated'})

        result = c.delete('{url}?id=0000000000'.format(url=self.url), headers={"DeviceAuthorization": self.token})

        self.assertEqual(result.status_code, 200)
        self.assertDictEqual(result.data, {'status': True, 'result': 'Device removed from database'})

        mobile_devices = MobileDevices.objects.all()
        serializer = MobileDevicesSerializer(mobile_devices, many=True)
        self.assertEqual(len(serializer.data), 0)

    def test_register_device_delete_no_identifier(self):
        c = Client()

        result = c.delete(self.url, headers={"DeviceAuthorization": self.token})

        self.assertEqual(result.status_code, 422)
        self.assertDictEqual(result.data, {'status': False, 'result': messages.invalid_query})

    def test_invalid_token(self):
        c = Client()

        result = c.post(self.url, headers={"DeviceAuthorization": 'invalid'})

        self.assertEqual(result.status_code, 403)
        self.assertEqual(result.reason_phrase, 'Forbidden')
