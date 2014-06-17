from django.shortcuts import render
from .models import HugoGene, DxGene, DxList
from .serializers import DxListSerializer
from rest_framework import viewsets

class HugoGeneViewSet(viewsets.ModelViewSet):
    model = HugoGene

class DxGeneViewSet(viewsets.ModelViewSet):
    model = DxGene

class DxListViewSet(viewsets.ModelViewSet):
    model = DxList
    serializer_class = DxListSerializer

