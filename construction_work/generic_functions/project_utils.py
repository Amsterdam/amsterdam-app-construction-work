from datetime import datetime, timedelta

from construction_work.models import Article, Project, WarningMessage


# TODO: create unit tests
def get_recent_articles_of_project(project: Project, article_max_age: int) -> list:
    from construction_work.serializers import ArticleSerializer, WarningMessagePublicSerializer

    all_articles = []

    datetime_now = datetime.now().astimezone()

    start_date = datetime_now - timedelta(days=int(article_max_age))
    end_date = datetime_now

    articles = project.article_set.filter(publication_date__range=[start_date, end_date]).all()
    article_serializer = ArticleSerializer(articles, many=True)
    all_articles.extend(article_serializer.data)

    warning_messages = project.warningmessage_set.filter(publication_date__range=[start_date, end_date]).all()
    warning_message_serializer = WarningMessagePublicSerializer(warning_messages, many=True)
    all_articles.extend(warning_message_serializer.data)

    return all_articles


def create_project_news_lookup(projects: list[Project], article_max_age):
    # Prefetch articles and warning messages within date range
    datetime_now = datetime.now().astimezone()
    start_date = datetime_now - timedelta(days=int(article_max_age))
    end_date = datetime_now

    # Setup lookup table
    project_news_mapping = {x.pk: [] for x in projects}

    def pre_fetch_news(model, pre_cursor, project_id_key):
        pre_fetched_qs = model.objects.filter(publication_date__range=[start_date, end_date]).values(
            "id", "modification_date", project_id_key
        )
        pre_fetched = list(pre_fetched_qs)

        # Remap articles to lookup table with project id as key
        for obj in pre_fetched:
            news_dict = {
                "meta_id": f"{pre_cursor}_{obj['id']}",
                "modification_date": str(obj["modification_date"]),
            }
            if obj[project_id_key] in [x.pk for x in projects]:
                project_news_mapping[obj[project_id_key]].append(news_dict)

    pre_fetch_news(Article, "a", "projects")
    pre_fetch_news(WarningMessage, "w", "project")

    return project_news_mapping
