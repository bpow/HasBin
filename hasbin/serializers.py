from rest_framework import serializers
import autocomplete_light
from .models import DxGene, DxGeneComment, DxList, HugoGene

class DxListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DxList
        fields = 'name description version official gene_phenotype_pairs'.split()
        depth = 2

class DxGeneSerializer(serializers.HyperlinkedModelSerializer):
	hugo_gene = serializers.ChoiceField(
		widget=autocomplete_light.TextWidget('HugoGeneAutocomplete'))
	class Meta:
		model = DxGene
		depth = 2

class HugoGeneSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = HugoGene