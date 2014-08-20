from django.shortcuts import render
from .models import HugoGene, DxGene, DxList
from .serializers import DxListSerializer, DxGeneSerializer, HugoGeneSerializer
from rest_framework import viewsets

class HugoGeneViewSet(viewsets.ReadOnlyModelViewSet):
    model = HugoGene
    serializer_class = HugoGeneSerializer

class DxGeneViewSet(viewsets.ModelViewSet):
    model = DxGene
    serializer_class = DxGeneSerializer

class DxListViewSet(viewsets.ModelViewSet):
    model = DxList
    serializer_class = DxListSerializer

