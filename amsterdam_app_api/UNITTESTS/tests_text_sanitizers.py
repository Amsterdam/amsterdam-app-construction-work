from django.test import TestCase
from amsterdam_app_api.GenericFunctions.TextSanitizers import TextSanitizers


class TestTextSanitizers(TestCase):
    def test_strip_html(self):
        html = '<div>mock data</div>'
        text_sanitizer = TextSanitizers()
        result = text_sanitizer.strip_html(html)

        self.assertEqual(result, 'mock data')

    def test_sentence_case_strip_spaces(self):
        sentence = ' mock '
        text_sanitizer = TextSanitizers()
        result = text_sanitizer.sentence_case(sentence, strip_spaces=True)

        self.assertEqual(result, 'Mock')

    def test_sentence_case_do_not_strip_spaces(self):
        sentence = ' mock '
        text_sanitizer = TextSanitizers()
        result = text_sanitizer.sentence_case(sentence, strip_spaces=False)

        self.assertEqual(result, ' mock ')
