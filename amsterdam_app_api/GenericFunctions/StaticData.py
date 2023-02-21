""" Class file for 'magic' -numbers, -data, -urls etc... """


class StaticData:
    """ Magic static data class methods """
    @staticmethod
    def districts():
        """ Convert city district numbers into names """
        return [
            {'id': 5398, 'name': 'Centrum'},
            {'id': 5520, 'name': 'Nieuw-West'},
            {'id': 5565, 'name': 'Noord'},
            {'id': 5399, 'name': 'Oost'},
            {'id': 5397, 'name': 'West'},
            {'id': 5396, 'name': 'Zuid'},
            {'id': 5393, 'name': 'Zuidoost'}
        ]

    @staticmethod
    def city_office_waiting_times_lookup_table():
        """ 'Magic' number table to convert city offices into ... magic number """
        return {
            '9': 'e9871a7716da02a4c20cfb06f9547005',
            '1': '5d9637689a8b902fa1a13acdf0006d26',
            '10': '081d6a38f46686905693fcd6087039f5',
            '11': '29e3b63d09d1f0c9a9c7238064c70790',
            '12': 'b4b178107cbc0c609d8d190bbdbdfb08',
            '8': 'b887a4d081821c4245c02f07e2de3290',
            '2': 'd338d28f8e6132ea2cfcf3e61785454c'
        }

    @staticmethod
    def urls():
        """ Some urls to simple names table """
        return {
            'address_to_gps': 'https://api.data.amsterdam.nl/atlas/search/adres/?q=',
            'waiting_times': 'https://wachttijdenamsterdam.nl/data'
        }
