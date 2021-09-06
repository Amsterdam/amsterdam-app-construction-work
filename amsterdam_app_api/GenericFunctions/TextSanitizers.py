import re
from bs4 import BeautifulSoup


class TextSanitizers:
    """ Reformat text (eg. strip html, capitalize, etc...)
    """
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

    @staticmethod
    def sentence_case(text, strip_spaces=True):
        """ Sentence case refers to titles in which only the first word has a capital letter, the same way a sentence
            is capitalized.
        """
        if strip_spaces is True:
            text = text.lstrip(' ').rstrip(' ')
            return str(text[0].upper() + text[1:])
        return str(text[0].upper() + text[1:])
