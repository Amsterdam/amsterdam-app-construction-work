""" Views for news routes """
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from construction_work.api_messages import Messages
from construction_work.generic_functions.request_must_come_from_app import (
    RequestMustComeFromApp,
)
from construction_work.generic_functions.static_data import StaticData
from construction_work.models import Article, WarningMessage
from construction_work.serializers import ArticleSerializer, ImagePublicSerializer
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
    projects_ids = request.GET.get("project_ids", None)
    sort_by = request.GET.get("sort_by", "publication_date")
    sort_order = request.GET.get("sort_order", "desc")

    limit = request.GET.get("limit", 0)
    if str(limit).isdigit() is False:
        return Response(data=message.invalid_query, status=status.HTTP_400_BAD_REQUEST)

    all_news = []

    # Collect articles
    article_values_params = ("id", "title", "publication_date", "image")
    if projects_ids:
        articles_list = Article.objects.filter(projects__id=projects_ids).values(
            *article_values_params
        )
    else:
        articles_list = Article.objects.values(*article_values_params)

    for obj in articles_list:
        obj["type"] = "news"
        obj["meta_id"] = f"a_{obj['id']}"
        obj.pop("id")
        obj["images"] = []
        if obj["image"] is not None:
            obj["images"].append(obj["image"])
        obj.pop("image", None)

    # Collect warnings
    image_serializer_context = {"base_url": StaticData.base_url(request)}

    warnings_qs = WarningMessage.objects
    if projects_ids:
        warnings_qs = warnings_qs.filter(project__id__in=projects_ids)
    warnings_qs = warnings_qs.prefetch_related("warningimage_set__images")

    warnings_list = []
    for warning in warnings_qs:
        warning_images = warning.warningimage_set.all()
        images = []
        for warning_image in warning_images:
            image_serializer = ImagePublicSerializer(
                instance=warning_image.images.all(),
                many=True,
                context=image_serializer_context,
            )
            image_dict = {"id": warning_image.pk, "sources": image_serializer.data}
            images.append(image_dict)

        warning_dict = {
            "title": warning.title,
            "publication_date": warning.publication_date,
            "type": "warning",
            "meta_id": f"w_{warning.pk}",
            "images": images,
        }
        warnings_list.append(warning_dict)

    all_news.extend(warnings_list)
    all_news.extend(articles_list)

    reverse = False
    if sort_order == "desc":
        reverse = True

    all_news = sorted(all_news, key=lambda x: x[sort_by], reverse=reverse)

    return Response(data=all_news, status=status.HTTP_200_OK)
