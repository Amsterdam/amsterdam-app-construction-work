""" UNITTESTS"""
from django.test import TestCase

from amsterdam_app_api.GenericFunctions.Distance import GeoPyDistance


class TestDistance(TestCase):
    """UNITTESTS"""

    def test_distance_valid(self):
        """Test distance computation with valid coordinates"""
        distance = GeoPyDistance((0.0, 0.0), (1.0, 1.0))
        self.assertEqual(distance.meter, 156899)
        self.assertEqual(distance.strides, 212025)

    def test_distance_in_valid(self):
        """Test distance computation with invalid coordinates"""
        distance = GeoPyDistance(("a", "b"), ("c", "d"))
        self.assertEqual(distance.meter, None)
        self.assertEqual(distance.strides, None)
