import socket
import time
from pact import Verifier


class PactTests:
    def __init__(self):
        self.provider_host = 'localhost'
        self.provider_port = 8000
        self.provider_url = 'http://{host}:{port}'.format(host=self.provider_host, port=self.provider_port)

        self.pact_contracts = [
            'consumer_iprox_scraper-provider_api_v1_ingest_asset.json',
            'consumer_iprox_scraper-provider_api_v1_ingest_office.json',
            'consumer_iprox_scraper-provider_api_v1_ingest_city_contact.json',
            'consumer_iprox_scraper-provider_api_v1_ingest_offices.json',
            'consumer_iprox_scraper-provider_api_v1_ingest_garbagecollector.json',
            'consumer_iprox_scraper-provider_api_v1_ingest_project.json',
            'consumer_iprox_scraper-provider_api_v1_ingest_image.json',
            'consumer_iprox_scraper-provider_api_v1_ingest_projects.json',
            'consumer_iprox_scraper-provider_api_v1_ingest_news.json'
        ]

    def wait_for_provider_is_alive(self):
        for i in range(3):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    s.connect((self.provider_host, self.provider_port))
                    return True
            except Exception as error:
                time.sleep(0.2)
        return False

    def run_test(self):
        if self.wait_for_provider_is_alive():
            for pact_contract in self.pact_contracts:
                verifier = Verifier(provider='amsterdam-app-modules',
                                    provider_base_url=self.provider_url)
                output, logs = verifier.verify_pacts('./{pact_contract}'.format(pact_contract=pact_contract))
                assert output == 0
        else:
            assert False is True


if __name__ == '__main__':
    pact_test = PactTests()
    pact_test.run_test()
