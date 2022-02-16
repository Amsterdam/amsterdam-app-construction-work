import io
import exifread
import pyheif
import whatimage
from io import BytesIO
from PIL import Image


class UnsupportedFormat(Exception):
    pass


class ImageConversion:
    def __init__(self, image_data, image_name=None):
        self.image_data = image_data
        self.target_sizes = [(320, 180), (768, 432), (1280, 720), (1920, 1080)]
        self.width = None
        self.height = None
        self.landscape = False
        self.image_format = None
        self.raw_data = None
        self.gps_info = {'longitude': None, 'latitude': None}
        self.images = {}
        self.image_name = image_name
        self.mime_type = 'image/jpg'

    def run(self):
        self.get_format()
        if not self.get_raw_data():
            # Bail-out! We caught an unsupported image format. Populate self.images with what we have...
            self.mime_type = ''
            self.set_image(data=self.image_data, width=None, height=None, key='original')
            return
        self.get_gps_info()
        self.scale_image()
        self.set_image(data=self.image_data, width=self.width, height=self.height, key='original')

    def get_format(self):
        # Get image format, returns None if unknown format
        self.image_format = whatimage.identify_image(self.image_data)

    def get_raw_data(self):
        # Get the raw image data and meta-data. Raise an exception for unsupported image formats
        try:
            if self.image_format in ['heic', 'avif']:
                image = pyheif.read(self.image_data)
                self.raw_data = Image.frombytes(mode=image.mode, size=image.size, data=image.data)
            elif self.image_format in ['jpeg', 'png']:
                image = BytesIO(self.image_data)
                self.raw_data = Image.open(image)
            else:
                raise UnsupportedFormat('Unsupported format')
            self.width = self.raw_data.width
            self.height = self.raw_data.height
            self.landscape = True if self.width > self.height else False
            return True
        except UnsupportedFormat:
            return False

    def get_gps_info(self):
        # Get GPS degrees, minutes and seconds from efix data and convert to decimal (negate if E or S)
        # If the image does not have any GPS data embedded, catch the exception
        try:
            tags = exifread.process_file(BytesIO(self.image_data))
            lat_ref = 'N' in tags.get('GPS GPSLatitudeRef').values
            lat_dms = tags.get('GPS GPSLatitude').values
            self.gps_info['latitude'] = (lat_dms[0] + lat_dms[1] / 60. + lat_dms[2] / 3600.) * (1 if lat_ref else -1)

            lon_ref = 'W' in tags.get('GPS GPSLongitudeRef').values
            lon_dms = tags.get('GPS GPSLongitude').values
            self.gps_info['longitude'] = (lon_dms[0] + lon_dms[1] / 60. + lon_dms[2] / 3600.) * (-1 if lon_ref else 1)
        except Exception as error:
            pass

    def calculate_new_size(self, target_size):
        # Keep aspect ratio whilst setting new width and height
        if self.landscape:
            width = target_size[0]
            ratio = (width / float(self.raw_data.size[0]))
            height = int((float(self.raw_data.size[1]) * float(ratio)))
        else:
            height = target_size[1]
            ratio = (height / float(self.raw_data.size[1]))
            width = int((float(self.raw_data.size[0]) * float(ratio)))

        return tuple((width, height))

    def scale_image(self):
        # For each desired image size convert the image and write the result into self.images dict
        for target_size in self.target_sizes:
            stream = io.BytesIO()
            valid_landscape_target = self.landscape and self.width > target_size[0]
            valid_portrait_target = not self.landscape and self.height > target_size[1]
            if valid_landscape_target or valid_portrait_target:
                new_size = self.calculate_new_size(target_size)
                img = self.raw_data.resize(new_size, Image.ANTIALIAS)
                img.save(stream, format='JPEG')
                key = '{width}x{height}'.format(width=new_size[0], height=new_size[1])
                self.set_image(data=stream.getvalue(), width=new_size[0], height=new_size[1], key=key)

    def set_image(self, data=None, width=None, height=None, key=None):
        # Populate self.images
        self.images[key] = {
            'data': data,
            'gps': self.gps_info,
            'width': width,
            'height': height,
            'landscape': self.landscape,
            'filename': '{key}-{image_name}'.format(key=key, image_name=self.image_name),
            'mime_type': self.mime_type
        }
