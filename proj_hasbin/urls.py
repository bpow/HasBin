from django.conf.urls import patterns, include, url
from hasbin.models import HugoGene, DxList, DxGene
from rest_framework import viewsets, routers

import autocomplete_light
autocomplete_light.autodiscover()

from django.contrib import admin
admin.autodiscover()

class HugoGeneViewSet(viewsets.ModelViewSet):
    model = HugoGene

class DxGeneViewSet(viewsets.ModelViewSet):
    model = DxGene

router = routers.DefaultRouter()

router.register(r'genes', HugoGeneViewSet)
router.register(r'dxgenes', DxGeneViewSet)

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'proj_hasbin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls)),
    #url(r'^', include('hasbin.urls')),
)
