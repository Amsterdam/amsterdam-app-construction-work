from amsterdam_app_api.FetchData.IproxIngestion import IproxIngestion


class CronJobs:
    def __init__(self):
        self.ingest_projects = IproxIngestion()

    def run(self):
        # Ingest data for projects 'bruggen' and 'kademuren'
        self.ingest_projects.start('brug')
        self.ingest_projects.start('kade')
        self.ingest_projects.start('stadsloket')


def run():
    cron = CronJobs()
    cron.run()
