""" Views for news routes """
from curses.ascii import isdigit

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.generic_functions.request_must_come_from_app import (
    RequestMustComeFromApp,
)
from construction_work.generic_functions.set_filter import SetFilter
from construction_work.generic_functions.sort import Sort
from construction_work.generic_functions.static_data import StaticData
from construction_work.models import Article, WarningMessage
from construction_work.models.asset_and_image import Image
from construction_work.models.warning_and_notification import WarningImage
from construction_work.serializers import (
    ArticleSerializer,
    ImageSerializer,
    WarningMessageMinimalSerializer,
    WarningMessagePublicSerializer,
)
from construction_work.swagger.swagger_views_iprox_news import (
    as_article,
    as_articles_get,
)

message = Messages()


@swagger_auto_schema(**as_article)
@api_view(["GET"])
# @RequestMustComeFromApp
def article(request):
    """Get a single article"""
    article_id = request.GET.get("id", None)
    if article_id is None:
        return Response(message.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    article_obj = Article.objects.filter(pk=article_id, active=True).first()
    if article_obj is None:
        return Response(message.no_record_found, status=status.HTTP_404_NOT_FOUND)

    serializer = ArticleSerializer(article_obj)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(**as_articles_get)
@api_view(["GET"])
# @RequestMustComeFromApp
def articles(request):
    """Get articles"""

    def filtering(data, article_type):
        _articles = []
        for item in data:
            _article = {
                "identifier": item["id"],
                "title": item["title"],
                "publication_date": item["publication_date"],
                "type": article_type if article_type == "warning" else item["type"],
            }
            if article_type == "news":
                _article["images"] = [item["image"]]
            else:
                _article["images"] = item["images"]

            _articles.append(_article)

        return _articles

    projects_ids = request.GET.get("project-ids", None)
    sort_by = request.GET.get("sort-by", "publication_date")
    sort_order = request.GET.get("sort-order", "desc")
    try:
        limit = int(request.GET.get("limit", 0))
    except Exception:
        limit = 0

    result = []
    if projects_ids is not None:
        project_identifiers = projects_ids.split(",")
        for project_identifier in project_identifiers:
            news_objects = list(
                Article.objects.filter(
                    project_identifier=project_identifier, active=True
                ).all()
            )
            for news_object in news_objects:
                result += filtering(
                    [ArticleSerializer(news_object, many=False).data], "news"
                )

            warning_objects = list(
                WarningMessage.objects.filter(
                    project_identifier=project_identifier
                ).all()
            )
            for warning_object in warning_objects:
                result += filtering(
                    [WarningMessagePublicSerializer(warning_object, many=False).data],
                    "warning",
                )
    else:
        news_objects = Article.objects.all()
        news_serializer = ArticleSerializer(news_objects, many=True)
        warning_objects = WarningMessage.objects.all()
        warning_serializer = WarningMessagePublicSerializer(warning_objects, many=True)
        result += filtering(news_serializer.data, "news")
        result += filtering(warning_serializer.data, "warning")

    # Get hostname for this server
    base_url = StaticData.base_url(request)

    result = Sort().list_of_dicts(result, key=sort_by, sort_order=sort_order)
    for item in result:
        item["publication_date"] = item["publication_date"]

        # Create image url for warning messages
        # if item["type"] == "warning":
        #     for image in item["images"]:
        #         for source in image["sources"]:
        #             source["url"] = f'{base_url}image?id={source["image_id"]}'

    if limit != 0:
        result = result[:limit]
    return Response({"status": True, "result": result}, status=200)


@swagger_auto_schema(**as_articles_get)
@api_view(["GET"])
# @RequestMustComeFromApp
def articles2(request):
    projects_ids = request.GET.get("project_ids", None)
    sort_by = request.GET.get("sort_by", "publication_date")
    sort_order = request.GET.get("sort_order", "desc")

    limit = request.GET.get("limit", 0)
    if str(limit).isdigit() is False:
        return Response(data=message.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    all_news = []
    # Get articles
    article_values_params = ("id", "title", "publication_date", "image")
    if projects_ids:
        articles_list = Article.objects.filter(projects__id=projects_ids).values(
            *article_values_params
        )
    else:
        articles_list = Article.objects.values(*article_values_params)

    for obj in articles_list:
        obj["meta_id"] = f"a_{obj['id']}"
        obj["images"] = []
        if obj["image"] is not None:
            obj["images"].append(obj["image"])
        obj.pop("image")

    # Get warnings

    # if projects_ids:
    #     warnings_qs = WarningMessage.objects.filter(project__id__in=projects_ids)
    # else:
    #     warnings_qs = WarningMessage.objects.all()
    # warning_serializer = WarningMessageMinimalSerializer(instance=warnings_qs, many=True)

    warnings_qs = WarningMessage.objects.prefetch_related("warningimage_set__images")

    warnings_list = []
    for warning in warnings_qs:
        images = [
            image
            for warning_image in warning.warningimage_set.all()
            for image in warning_image.images.all()
        ]
        # TODO: format images the same way as article images, with working url
        image_serializer = ImageSerializer(instance=images, many=True)

        warning_dict = {
            "id": warning.pk,
            "title": warning.title,
            "publication_date": warning.publication_date,
            "images": image_serializer.data,
        }
        warnings_list.append(warning_dict)

    # all_news.extend(articles_list)
    all_news.extend(warnings_list)

    return Response(data=all_news, status=status.HTTP_200_OK)
