from django.test import TestCase
from amsterdam_app_api.UNITTESTS.mock_data import TestData
from amsterdam_app_api.FetchData.IproxRecursion import IproxRecursion


class TestIproxRecursion(TestCase):
    def __init__(self, *args, **kwargs):
        super(TestIproxRecursion, self).__init__(*args, **kwargs)
        self.data = TestData()

    def test_recursion(self):
        iprox_recursion = IproxRecursion()
        result = iprox_recursion.filter(self.data.iprox_recursion, [], targets=['Target'])
        expected_result = [{'Target': []}, {'Target': {'Nam': 'Target', 'veld': {}}}]

        self.assertEqual(result, expected_result)
