from datetime import datetime, timedelta

from construction_work.models import Article, Project, WarningMessage


# TODO: create unit tests
def get_recent_articles_of_project(project: Project, article_max_age: int, minimal=False) -> list:
    # TODO: This import is here to circumvent circular imports. This is a code smell.
    from construction_work.serializers import (
        ArticleMinimalSerializer,
        ArticleSerializer,
        WarningMessageMinimalSerializer,
        WarningMessagePublicSerializer,
    )

    all_articles = []

    datetime_now = datetime.now().astimezone()

    # Set end_date one day from now, this makes sure warning messages that are just made are taken into account too.
    # The reason is that "publication_date = models.DateTimeField(auto_now_add=True)" is set in the model.
    start_date = datetime_now - timedelta(days=int(article_max_age))
    end_date = datetime_now + timedelta(days=1)

    articles = project.article_set.filter(publication_date__range=[start_date, end_date]).all()
    if minimal is True:
        article_serializer = ArticleMinimalSerializer(articles, many=True)
    else:
        article_serializer = ArticleSerializer(articles, many=True)
    all_articles.extend(article_serializer.data)

    warning_messages = project.warningmessage_set.filter(publication_date__range=[start_date, end_date]).all()
    if minimal is True:
        warning_message_serializer = WarningMessageMinimalSerializer(warning_messages, many=True)
    else:
        warning_message_serializer = WarningMessagePublicSerializer(warning_messages, many=True)
    all_articles.extend(warning_message_serializer.data)

    return all_articles


# TODO: create unit tests
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
