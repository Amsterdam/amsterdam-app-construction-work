from django.urls import path
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from amsterdam_app_api.views import views_ingest, views_iprox_news, views_iprox_projects, views_messages, views_generic, \
    views_user, views_project_manager, views_mobile_devices

schema_view = get_schema_view(
   openapi.Info(
      title="Amsterdam APP Backend API",
      default_version='v1',
      description="API backend server for Amsterdam App."
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

""" Base path: /api/v1
"""

urlpatterns = [
    # Path to obtain a new access and refresh token (refresh token expires after 24h)
    path('get-token/', csrf_exempt(TokenObtainPairView.as_view()), name='token_obtain_pair'),

    # Submit your refresh token to this path to obtain a fresh access token
    path('refresh-token/', csrf_exempt(TokenRefreshView.as_view()), name='token_refresh'),

    path('user/password', csrf_exempt(views_user.change_password)),

    # Swagger (drf-yasg framework)
    url(r'^apidocs$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Project(s)
    path('projects', csrf_exempt(views_iprox_projects.projects)),
    path('project/details', csrf_exempt(views_iprox_projects.project_details)),
    path('project/news', csrf_exempt(views_iprox_news.news)),

    # Ingestion
    path('ingest', csrf_exempt(views_ingest.ingest_projects)),

    # Image & Assets
    path('image', csrf_exempt(views_generic.image)),
    path('asset', csrf_exempt(views_generic.asset)),

    # Mobile devices (used for CRUD devices for push-notifications)
    path('device_registration', csrf_exempt(views_mobile_devices.crud)),

    # Project Manager (used to CRUD a project manager for notifications)
    path('project/manager', csrf_exempt(views_project_manager.crud)),

    # Warning message
    path('project/warning', csrf_exempt(views_messages.warning_message_crud)),
    path('project/warning/image', csrf_exempt(views_messages.warning_messages_image_upload)),

    # Notification ('teaser' pointing to news- or warning article)
    path('notification', csrf_exempt(views_messages.notification_post)),
    path('notifications', csrf_exempt(views_messages.notification_get))
]
