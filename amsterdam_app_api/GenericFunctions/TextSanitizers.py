import re
from bs4 import BeautifulSoup


class TextSanitizers:
    @staticmethod
    def strip_html(html):
        """
        Strip all html tags from given string

        :param html: string
        :return: string
        """

        # Use BeautifulSoup to strip any html tags
        soup = BeautifulSoup(html, features='html.parser')
        text = soup.get_text(separator=u'\n\n', strip=True)

        # Cleanup text a bit
        regex_1 = re.compile('\.Zie ook')
        regex_2 = re.compile('â')
        regex_3 = re.compile('\b\.\b')
        text = re.sub(regex_1, '. Zie ook: ', text)
        text = re.sub(regex_2, '\'', text)
        text = re.sub(regex_3, '. ', text)
        return text
