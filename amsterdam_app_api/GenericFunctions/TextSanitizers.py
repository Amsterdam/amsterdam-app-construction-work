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


if __name__ == '__main__':
    markup = """
              <div>
                <p>De monumentale Berlagebrug uit 1932 is toe aan groot onderhoud. Bij het bedienen van de brug treden soms storingen op waardoor de brug niet verder open of dicht kan. Ook klemt de brug op warme zomerdagen waardoor we deze niet kunnen openen zonder koeling. Daarom komt er een nieuwe bewegingsconstructie en vervangen we het beweegbare brugdek.</p>
                <p>In 2022 starten we met de renovatie van de monumentale onderdelen van de Berlagebrug. We knappen de smeedijzeren leuningen, de masten, het metselwerk en het natuursteen op. We renoveren de aansluitende kadeconstructies, botenloodsen en kademuur aan de Amsteldijk Berlagebrug. De Schollenbrug wordt ook opgeknapt. Deze werkzaamheden hebben geen gevolgen op de doorstroming van het verkeer.</p>
                <p>De brug sluiten we in 2023 een aantal maanden af voor alle verkeer. De Berlagebrug is een drukke fietsverbinding. En daarom komt er tijdens deze afsluiting een hulpbrug voor fietsers en voetgangers aan de noordzijde van de Berlagebrug. Het GVB gaat tramrails en bovenleidingen op de kruisingen naast de Berlagebrug vervangen. Daarnaast verbeteren we de fietsoversteek kruising Amsteldijk en Vrijheidslaan. Door deze werkzaamheden allemaal rond de zomer van 2023 uit te voeren, beperken we de totale overlast voor de buurt.</p>
              </div>
              """
    parse = TextSanitizers.strip_html(markup)
    pass
