""" Url patterns for API """
from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from construction_work.views import (
    views_generic,
    views_ingest,
    views_iprox_news,
    views_iprox_projects,
    views_messages,
    views_mobile_devices,
    views_project_manager,
    views_user,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Amsterdam APP - Construction Work API",
        default_version="v1",
        description="API backend server for construction work within the Amsterdam App.",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

""" Base path: /api/v1
"""

urlpatterns = [
    # Path to obtain a new access and refresh token (refresh token expires after 24h)
    path(
        "get-token/",
        csrf_exempt(TokenObtainPairView.as_view()),
        name="token_obtain_pair",
    ),
    # Submit your refresh token to this path to obtain a fresh access token
    path("refresh-token/", csrf_exempt(TokenRefreshView.as_view()), name="token_refresh"),
    path("user/password", csrf_exempt(views_user.change_password)),
    # Swagger (drf-yasg framework)
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^apidocs/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # Project(s)
    path("projects", csrf_exempt(views_iprox_projects.projects)),
    path("projects/search", csrf_exempt(views_iprox_projects.projects_search)),
    path("projects/follow", csrf_exempt(views_iprox_projects.project_follow)),
    path("projects/followed/articles", csrf_exempt(views_iprox_projects.projects_followed_articles)),
    path("projects/follow", csrf_exempt(views_iprox_projects.project_follow)),
    path(
        "projects/followed/articles",
        csrf_exempt(views_iprox_projects.projects_followed_articles),
    ),
    # Project details(s)
    path("project/details", csrf_exempt(views_iprox_projects.project_details)),
    # News
    path("project/news", csrf_exempt(views_iprox_news.article)),
    # Articles belonging to projects (news and warnings)
    path("articles", csrf_exempt(views_iprox_news.articles)),
    # Ingestion
    path("ingest/garbagecollector", csrf_exempt(views_ingest.garbage_collector)),
    path("ingest/project", csrf_exempt(views_ingest.etl_project)),
    path("ingest/article", csrf_exempt(views_ingest.etl_article)),
    # Image & Assets
    path("image", csrf_exempt(views_generic.image)),
    # Mobile devices (used for C..D devices for push-notifications)
    path("device/register", csrf_exempt(views_mobile_devices.device_register)),
    # Project Manager (used to CRUD a project manager for notifications)
    path("project/manager", csrf_exempt(views_project_manager.crud)),
    # Warning message
    path("project/warning", csrf_exempt(views_messages.warning_message_crud)),
    path("project/warnings", csrf_exempt(views_messages.warning_messages_get)),
    path(
        "project/warning/image",
        csrf_exempt(views_messages.warning_messages_image_upload),
    ),
    # Notification ('teaser' pointing to news- or warning article)
    path("notification", csrf_exempt(views_messages.notification_post)),
    path("notifications", csrf_exempt(views_messages.notification_get)),
    path("__debug__/", include("debug_toolbar.urls")),
]
