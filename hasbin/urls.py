from django.conf.urls import patterns, include, url
from .views import HugoGeneViewSet, DxListViewSet, DxGeneViewSet
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'gene', HugoGeneViewSet)
router.register(r'dxgene', DxGeneViewSet)
router.register(r'dxlist', DxListViewSet)

urlpatterns = patterns('',
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

