from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PackagesViewSet, package_detail
from django.conf.urls.static import static
from django.conf import settings

router = DefaultRouter()
router.register(r'packages', PackagesViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('package/<int:id>/', package_detail, name='package_detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
