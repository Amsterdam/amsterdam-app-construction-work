from datetime import datetime, timedelta
from construction_work.models.project import Project


# TODO: create unit tests
def get_recent_articles_of_project(project: Project, article_max_age: int, article_serializer, warning_message_serializer) -> dict:    
    all_articles = []

    datetime_now = datetime.now().astimezone()

    start_date = datetime_now - timedelta(days=int(article_max_age))
    end_date = datetime_now
    
    articles = project.article_set.filter(publication_date__range=[start_date, end_date]).all()
    article_serializer = article_serializer(articles, many=True)
    all_articles.extend(article_serializer.data)

    warning_messages = project.warningmessage_set.filter(publication_date__range=[start_date, end_date]).all()
    warning_message_serializer = warning_message_serializer(warning_messages, many=True)
    all_articles.extend(warning_message_serializer.data)

    return all_articles
