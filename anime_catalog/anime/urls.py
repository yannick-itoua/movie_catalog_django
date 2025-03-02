from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnimeViewSet

router = DefaultRouter()
router.register(r'anime', AnimeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    #path('load-anime/', AnimeViewSet.as_view({'post': 'create'}), name='load-anime'),  # Nouveau endpoint
]
