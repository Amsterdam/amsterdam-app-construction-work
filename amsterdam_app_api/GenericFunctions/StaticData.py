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
    def urls():
        return {
            'address_to_gps': 'https://api.data.amsterdam.nl/atlas/search/adres/?q='
        }