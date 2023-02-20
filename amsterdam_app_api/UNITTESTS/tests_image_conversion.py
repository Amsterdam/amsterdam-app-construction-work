""" UNITTESTS """
import os
import base64
from django.test import TestCase
from amsterdam_app_api.GenericFunctions.ImageConversion import ImageConversion


class TestImageConversion(TestCase):
    """ UNITTESTS """
    @staticmethod
    def read_file(filename):
        """ Read file data """
        with open(filename, 'rb') as f:
            data = f.read()
        return data

    def test_heic_gps_landscape(self):
        """ test conversion of a heic image in landscape format """
        path = '{cwd}/amsterdam_app_api/UNITTESTS/image_data/landscape.HEIC'.format(cwd=os.getcwd())
        image_data = self.read_file(path)
        image_conversion = ImageConversion(image_data, 'landscape.HEIC')
        image_conversion.run()

        self.assertEqual(len(image_conversion.images), 6)

        self.assertDictEqual(image_conversion.gps_info, {'lon': None, 'lat': None})
        self.assertEqual(image_conversion.landscape, True)

        self.assertEqual(image_conversion.images['original']['width'], 4032)
        self.assertEqual(image_conversion.images['original']['height'], 3024)
        self.assertEqual(image_conversion.images['original']['filename'], 'original-landscape.HEIC')
        self.assertEqual(image_conversion.images['original']['mime_type'], 'image/heic')

        self.assertEqual(image_conversion.images['original-size-jpeg']['width'], 4032)
        self.assertEqual(image_conversion.images['original-size-jpeg']['height'], 3024)
        self.assertEqual(image_conversion.images['original-size-jpeg']['filename'], 'original-size-jpeg-landscape.HEIC')
        self.assertEqual(image_conversion.images['original-size-jpeg']['mime_type'], 'image/jpeg')

        self.assertEqual(image_conversion.images['320x240']['width'], 320)
        self.assertEqual(image_conversion.images['320x240']['height'], 240)
        self.assertEqual(image_conversion.images['320x240']['filename'], '320x240-landscape.HEIC')
        self.assertEqual(image_conversion.images['320x240']['mime_type'], 'image/jpeg')

        self.assertEqual(image_conversion.images['768x576']['width'], 768)
        self.assertEqual(image_conversion.images['768x576']['height'], 576)
        self.assertEqual(image_conversion.images['768x576']['filename'], '768x576-landscape.HEIC')
        self.assertEqual(image_conversion.images['768x576']['mime_type'], 'image/jpeg')

        self.assertEqual(image_conversion.images['1280x960']['width'], 1280)
        self.assertEqual(image_conversion.images['1280x960']['height'], 960)
        self.assertEqual(image_conversion.images['1280x960']['filename'], '1280x960-landscape.HEIC')
        self.assertEqual(image_conversion.images['1280x960']['mime_type'], 'image/jpeg')

        self.assertEqual(image_conversion.images['1920x1440']['width'], 1920)
        self.assertEqual(image_conversion.images['1920x1440']['height'], 1440)
        self.assertEqual(image_conversion.images['1920x1440']['filename'], '1920x1440-landscape.HEIC')
        self.assertEqual(image_conversion.images['1920x1440']['mime_type'], 'image/jpeg')

    def test_jpg_gps_portrait(self):
        """ Test conversion of a jpg image in portrait format with embedded coordinates """
        path = '{cwd}/amsterdam_app_api/UNITTESTS/image_data/portrait.jpg'.format(cwd=os.getcwd())
        image_data = self.read_file(path)
        image_conversion = ImageConversion(image_data, 'portrait.jpg')
        image_conversion.run()

        self.assertEqual(len(image_conversion.images), 5)

        self.assertDictEqual(image_conversion.gps_info, {'lon': 6.182558333333334, 'lat': 52.14435833333333})
        self.assertEqual(image_conversion.landscape, False)

        self.assertEqual(image_conversion.images['original']['width'], 3024)
        self.assertEqual(image_conversion.images['original']['height'], 4032)
        self.assertEqual(image_conversion.images['original']['filename'], 'original-portrait.jpg')
        self.assertEqual(image_conversion.images['original']['mime_type'], 'image/jpeg')

        self.assertEqual(image_conversion.images['135x180']['width'], 135)
        self.assertEqual(image_conversion.images['135x180']['height'], 180)
        self.assertEqual(image_conversion.images['135x180']['filename'], '135x180-portrait.jpg')
        self.assertEqual(image_conversion.images['135x180']['mime_type'], 'image/jpeg')

        self.assertEqual(image_conversion.images['324x432']['width'], 324)
        self.assertEqual(image_conversion.images['324x432']['height'], 432)
        self.assertEqual(image_conversion.images['324x432']['filename'], '324x432-portrait.jpg')
        self.assertEqual(image_conversion.images['324x432']['mime_type'], 'image/jpeg')

        self.assertEqual(image_conversion.images['540x720']['width'], 540)
        self.assertEqual(image_conversion.images['540x720']['height'], 720)
        self.assertEqual(image_conversion.images['540x720']['filename'], '540x720-portrait.jpg')
        self.assertEqual(image_conversion.images['540x720']['mime_type'], 'image/jpeg')

        self.assertEqual(image_conversion.images['810x1080']['width'], 810)
        self.assertEqual(image_conversion.images['810x1080']['height'], 1080)
        self.assertEqual(image_conversion.images['810x1080']['filename'], '810x1080-portrait.jpg')
        self.assertEqual(image_conversion.images['810x1080']['mime_type'], 'image/jpeg')

    def test_avif_no_gps_portrait(self):
        """ test converting a avif image without gps coordinates in portrait mode """
        path = '{cwd}/amsterdam_app_api/UNITTESTS/image_data/portrait.avif'.format(cwd=os.getcwd())
        image_data = self.read_file(path)
        image_conversion = ImageConversion(image_data, 'portrait.avif')
        image_conversion.run()

        self.assertEqual(len(image_conversion.images), 6)

        self.assertDictEqual(image_conversion.gps_info, {'lon': None, 'lat': None})
        self.assertEqual(image_conversion.landscape, False)

        self.assertEqual(image_conversion.images['original']['width'], 3024)
        self.assertEqual(image_conversion.images['original']['height'], 4032)
        self.assertEqual(image_conversion.images['original']['filename'], 'original-portrait.avif')
        self.assertEqual(image_conversion.images['original']['mime_type'], 'image/avif')

        self.assertEqual(image_conversion.images['original-size-jpeg']['width'], 3024)
        self.assertEqual(image_conversion.images['original-size-jpeg']['height'], 4032)
        self.assertEqual(image_conversion.images['original-size-jpeg']['filename'], 'original-size-jpeg-portrait.avif')
        self.assertEqual(image_conversion.images['original-size-jpeg']['mime_type'], 'image/jpeg')

        self.assertEqual(image_conversion.images['135x180']['width'], 135)
        self.assertEqual(image_conversion.images['135x180']['height'], 180)
        self.assertEqual(image_conversion.images['135x180']['filename'], '135x180-portrait.avif')
        self.assertEqual(image_conversion.images['135x180']['mime_type'], 'image/jpeg')

        self.assertEqual(image_conversion.images['324x432']['width'], 324)
        self.assertEqual(image_conversion.images['324x432']['height'], 432)
        self.assertEqual(image_conversion.images['324x432']['filename'], '324x432-portrait.avif')
        self.assertEqual(image_conversion.images['324x432']['mime_type'], 'image/jpeg')

        self.assertEqual(image_conversion.images['540x720']['width'], 540)
        self.assertEqual(image_conversion.images['540x720']['height'], 720)
        self.assertEqual(image_conversion.images['540x720']['filename'], '540x720-portrait.avif')
        self.assertEqual(image_conversion.images['540x720']['mime_type'], 'image/jpeg')

        self.assertEqual(image_conversion.images['810x1080']['width'], 810)
        self.assertEqual(image_conversion.images['810x1080']['height'], 1080)
        self.assertEqual(image_conversion.images['810x1080']['filename'], '810x1080-portrait.avif')
        self.assertEqual(image_conversion.images['810x1080']['mime_type'], 'image/jpeg')

    def test_unsupported_format(self):
        """ Test for unsupported image format (erroneous data) """
        image_data = b'0xff'
        image_conversion = ImageConversion(image_data, 'foobar')
        image_conversion.run()

        self.assertEqual(len(image_conversion.images), 0)
        self.assertDictEqual(image_conversion.images, {})

    def test_RGBA_to_RGB(self):
        """ Test converting alpha channel to plain (RGB format) """
        base64_data = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+P+/HgAFhAJ/wlseKgAAAABJRU5ErkJggg=='
        image_data = base64.b64decode(base64_data)
        image_conversion = ImageConversion(image_data, 'foobar')
        image_conversion.run()

        self.assertEqual(len(image_conversion.images), 2)
        self.assertEqual(image_conversion.mime_type, 'image/png')
        self.assertEqual(image_conversion.landscape, False)
        self.assertEqual(image_conversion.image_format, 'png')
        self.assertEqual(image_conversion.aspect_ratio, 1.0)
        self.assertEqual(image_conversion.height, 1)
        self.assertEqual(image_conversion.width, 1)
        self.assertDictEqual(image_conversion.gps_info, {'lat': None, 'lon': None})
