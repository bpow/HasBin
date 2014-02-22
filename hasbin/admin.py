from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
import autocomplete_light
import hasbin.models as models


class DxGeneReferenceInline(admin.TabularInline):
    model = models.DxGeneReference


class DxGeneCommentInline(admin.TabularInline):
    model = models.DxGeneComment


class DxGeneAdmin(SimpleHistoryAdmin):
    inlines = [DxGeneReferenceInline, DxGeneCommentInline]
    form = autocomplete_light.modelform_factory(models.DxGene)


class BinnedGeneReferenceInline(admin.TabularInline):
    model = models.BinnedGeneReference


class BinnedGeneCommentInline(admin.TabularInline):
    model = models.BinnedGeneComment


class BinnedGeneAdmin(SimpleHistoryAdmin):
    inlines = [BinnedGeneReferenceInline, BinnedGeneCommentInline]
    form = autocomplete_light.modelform_factory(models.BinnedGene)


admin.site.register(models.DxGene, DxGeneAdmin)
admin.site.register(models.BinnedGene, BinnedGeneAdmin)

