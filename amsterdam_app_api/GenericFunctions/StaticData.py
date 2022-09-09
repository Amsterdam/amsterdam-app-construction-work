class StaticData:
    @staticmethod
    def districts():
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
        return {
            '9': 'Stadsloket Centrum',
            '1': 'Stadsloket Nieuw-West',
            '10': 'Stadsloket Noord',
            '11': 'Stadsloket Oost',
            '12': 'Stadsloket West',
            '8': 'Stadsloket Zuid',
            '2': 'Stadsloket Zuidoost'
        }

    @staticmethod
    def urls():
        return {
            'address_to_gps': 'https://api.data.amsterdam.nl/atlas/search/adres/?q=',
            'waiting_times': 'https://wachttijdenamsterdam.nl/data'
        }