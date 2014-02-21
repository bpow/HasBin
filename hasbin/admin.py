from django.contrib import admin
import hasbin.models as models

admin.site.register((
    models.HugoGene,
    models.DxList,
    models.BinnedGene,
))
