""" Views for news routes """
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from amsterdam_app_api.api_messages import Messages
from amsterdam_app_api.GenericFunctions.SetFilter import SetFilter
from amsterdam_app_api.GenericFunctions.Sort import Sort
from amsterdam_app_api.GenericFunctions.StaticData import StaticData
from amsterdam_app_api.models import Article, WarningMessages
from amsterdam_app_api.serializers import ArticleSerializer, WarningMessagesExternalSerializer
from amsterdam_app_api.swagger.swagger_views_iprox_news import as_article, as_articles_get, as_news_by_project_id

message = Messages()


@swagger_auto_schema(**as_news_by_project_id)
@api_view(["GET"])
def news_by_project_id(request):
    """
    Get a list of news items. Narrow down by query param: identifier (from project details)
    """
    project_identifier = request.GET.get("project-identifier", None)
    sort_by = request.GET.get("sort-by", "publication_date")
    sort_order = request.GET.get("sort-order", "desc")

    # Set filter
    query_filter = SetFilter(project_identifier=project_identifier, active=True).get()

    # Return filtered result or all projects
    news_objects = Article.objects.filter(**query_filter).all()

    serializer = ArticleSerializer(news_objects, many=True)
    result = Sort().list_of_dicts(serializer.data, key=sort_by, sort_order=sort_order)
    return Response({"status": True, "result": result}, status=200)


@swagger_auto_schema(**as_article)
@api_view(["GET"])
def article(request):
    """
    Get a single article
    """
    identifier = request.GET.get("id", None)
    if identifier is None:
        return Response({"status": False, "result": message.invalid_query}, status=422)

    article_object = Article.objects.filter(identifier=identifier, active=True).first()
    if article_object is None:
        return Response({"status": False, "result": message.no_record_found}, status=404)

    serializer = ArticleSerializer(article_object, many=False)
    return Response({"status": True, "result": serializer.data}, status=200)


@swagger_auto_schema(**as_articles_get)
@api_view(["GET"])
def articles(request):
    """Get articles"""

    def filtering(data, article_type):
        _articles = []
        for item in data:
            _article = {
                "identifier": item["identifier"],
                "title": item["title"],
                "publication_date": item["publication_date"],
                "type": article_type if article_type == "warning" else item["type"],
            }
            if article_type == "news":
                _article["image"] = next(
                    iter([x for x in item["images"] if x["type"] in ["main", "banner", "header"]]), None
                )
            else:
                _article["images"] = item["images"]
            _articles.append(_article)

        return _articles

    query_params = request.GET.get("project-ids", None)
    sort_by = request.GET.get("sort-by", "publication_date")
    sort_order = request.GET.get("sort-order", "desc")
    try:
        limit = int(request.GET.get("limit", default=0))
    except Exception:
        limit = 0

    result = []
    if query_params is not None:
        project_identifiers = query_params.split(",")
        for project_identifier in project_identifiers:
            news_objects = list(Article.objects.filter(project_identifier=project_identifier, active=True).all())
            for news_object in news_objects:
                result += filtering([ArticleSerializer(news_object, many=False).data], "news")

            warning_objects = list(WarningMessages.objects.filter(project_identifier=project_identifier).all())
            for warning_object in warning_objects:
                result += filtering([WarningMessagesExternalSerializer(warning_object, many=False).data], "warning")
    else:
        news_objects = Article.objects.all()
        news_serializer = ArticleSerializer(news_objects, many=True)
        warning_objects = WarningMessages.objects.all()
        warning_serializer = WarningMessagesExternalSerializer(warning_objects, many=True)
        result += filtering(news_serializer.data, "news")
        result += filtering(warning_serializer.data, "warning")

    # Get hostname for this server
    base_url = StaticData.base_url(request)

    result = Sort().list_of_dicts(result, key=sort_by, sort_order=sort_order)
    for item in result:
        item["publication_date"] = item["publication_date"]

        # Create image url for warning messages
        if item["type"] == "warning":
            for image in item["images"]:
                for source in image["sources"]:
                    source["url"] = f'{base_url}image?id={source["image_id"]}'

    if limit != 0:
        result = result[:limit]
    return Response({"status": True, "result": result}, status=200)
