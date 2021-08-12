from amsterdam_app_api.FetchData.Projects import IngestProjects


class CronJobs:
    def __init__(self):
        self.ingest_projects = IngestProjects()

    def run(self):
        # Ingest data for projects 'bruggen' and 'kademuren'
        self.ingest_projects.get_set_projects('brug')
        self.ingest_projects.get_set_projects('kade')


def run():
    cron = CronJobs()
    cron.run()
