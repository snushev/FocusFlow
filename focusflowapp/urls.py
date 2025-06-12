from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import HabitViewSet, HabitEntryViewSet, TokenLoginView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger initialization
schema_view = get_schema_view(
   openapi.Info(
      title="TaskHub API",
      default_version='v1',
      description="API for managing projects, tasks, tags and comments.",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# Router initialization
router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habit')
router.register(r'habit-entry', HabitEntryViewSet, basename='habit-entry')

urlpatterns = [
    path('login/', TokenLoginView.as_view(), name='login'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + router.urls