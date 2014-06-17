from rest_framework import serializers
from .models import DxGene, DxGeneComment, DxList, HugoGene

class DxListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DxList
        fields = 'name description version official gene_phenotype_pairs'.split()
        depth = 2
