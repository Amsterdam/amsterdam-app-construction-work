from amsterdam_app_api.FetchData.IproxIngestion import IproxIngestion


class CronJobs:
    def __init__(self):
        self.ingest_projects = IproxIngestion()

    def run(self):
        # Ingest data for projects 'bruggen' and 'kademuren'
        self.ingest_projects.get_set_projects('brug')
        self.ingest_projects.get_set_projects('kade')


def run():
    cron = CronJobs()
    cron.run()
