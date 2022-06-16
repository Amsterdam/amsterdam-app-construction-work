from django.test import Client
from django.test import TestCase


class TestSwaggerDefinitions(TestCase):
    def test_swagger(self):
        c = Client()
        try:
            response = c.get('/api/v1/apidocs', {'format': 'openapi'})
            self.assertEqual(response.status_code, 301)
        except:  # pragma: no cover
            # Should never happen, it means your swagger definitions are erroneous
            self.assertEqual(True, False)
