""" unit_tests"""
from django.test import TestCase

from construction_work.generic_functions.gps_utils import get_distance


class TestDistance(TestCase):
    """unit_tests"""

    def test_distance_valid(self):
        """Test distance computation with valid coordinates"""
        meter, strides = get_distance((0.0, 0.0), (1.0, 1.0))
        self.assertEqual(meter, 156899)
        self.assertEqual(strides, 212025)

    def test_distance_in_valid(self):
        """Test distance computation with invalid coordinates"""
        meter, strides = get_distance(("a", "b"), ("c", "d"))
        self.assertEqual(meter, None)
        self.assertEqual(strides, None)
