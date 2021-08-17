from django.urls import path
from django.conf.urls import url
from amsterdam_app_api import views


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


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
    # Swagger (drf-yasg)
    url(r'^apidocs$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Projects
    path('projects', views.projects),
    path('projects/ingest', views.ingest_projects),
    path('project/details', views.project_details),

    # Image
    path('image', views.image)
]
