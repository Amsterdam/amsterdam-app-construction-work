""" Iprox garbage collector """
from datetime import timedelta

from construction_work.models import Article, Project


class GarbageCollector:
    """Remove old scraped data from database if upstream has removed it too."""

    def __init__(self, last_scrape_time=None):
        self.last_scrape_time = last_scrape_time

    def collect_iprox(self):
        """Call all iprox dataset garbage collectors one by one"""
        report_projects = {}
        report_news = {}

        # If there's no path, projects might be de-activated un-rightfully
        news = list(Article.objects.all())
        report_news = self.garbage_collect_iprox(
            news,
            model=Article,
            model_name="News",
            id_name="identifier",
        )

        projects = list(Project.objects.all())
        report_projects = self.garbage_collect_iprox(
            projects,
            model=Project,
            model_name="Projects",
            id_name="project_id",
        )

        return {
            "projects": report_projects,
            "news": report_news,
        }

    def garbage_collect_iprox(
        self, data_objects, model=None, model_name=None, id_name=None
    ):
        """Generic garbage collections method"""
        report = {}
        for data_object in data_objects:
            # Check if we've seen this project anywhere in the last week, if not -> delete!
            if (
                getattr(data_object, "last_seen") + timedelta(days=7)
                <= self.last_scrape_time
            ):
                # If there are siblings then they are cascaded deleted
                report[str(getattr(data_object, id_name))] = "deleted"
                data_object.delete()

            # We've seen the object (again!), mark active=true
            elif getattr(data_object, "last_seen") >= self.last_scrape_time:
                data = {"active": True}
                model.objects.filter(pk=getattr(data_object, id_name)).update(**data)
                report[getattr(data_object, id_name)] = "activated"

            # If we haven't seen the object in last scrape, assume it's deleted from iprox and mark inactive
            elif getattr(data_object, "last_seen") < self.last_scrape_time:
                data = {"active": False}
                if model_name == "News":
                    model.objects.filter(
                        identifier=getattr(data_object, id_name),
                        project_identifier=getattr(data_object, "project_identifier"),
                    ).update(**data)
                else:
                    model.objects.filter(pk=getattr(data_object, id_name)).update(
                        **data
                    )

                report[getattr(data_object, id_name)] = "deactivated"

        return report
