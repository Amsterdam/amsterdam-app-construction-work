""" EARTH_RADIUS = 6371.009

    major (km)  minor (km)      flattening
    6378.137    6356.7523142    1 / 298.257223563

    Vincenty's formulae are two related iterative methods used in geodesy to calculate the distance between two
    points on the surface of a spheroid, developed by Thaddeus Vincenty (1975a). They are based on the assumption
    that the figure of the Earth is an oblate spheroid, and hence are more accurate than methods that assume a
    spherical Earth, such as great-circle distance.

    The most accurate and widely used globally-applicable model for the earth ellipsoid is WGS-84, used in this
    script. Other ellipsoids offering a better fit to the local geoid include Airy (1830) in the UK, International
    1924 in much of Europe, Clarke (1880) in Africa, and GRS-67 in South America. America (NAD83) and Australia
    (GDA) use GRS-80, functionally equivalent to the WGS-84 ellipsoid.

    Latitude must be in the [-90; 90] range.
    Longitude must be in the [-180; 180] range.

    Strides:

    An average man's stride length is 78 centimeters, while a woman's average stride length is 70 centimeters. In
    To compute the distance in steps this class uses the average length of 0.74 meter
"""

import geopy.distance


class Distance:
    """ Calculate distance between two gps coordinates """
    def __init__(self, coords_1, coords_2):
        """ :param coords_1: tuple(52.2296756, 21.0122287)
            :param coords_2: tuple(52.406374, 16.9251681)
        """
        self.meter = None
        self.strides = None

        if not any(elem is None for elem in [coords_1[0], coords_1[1], coords_2[0], coords_2[1]]):
            try:
                self.meter = int(geopy.distance.geodesic(coords_1, coords_2).km * 1000)
                self.strides = int(self.meter / 0.74)
            except ValueError:
                pass
            except Exception as error:
                print(error, flush=True)
