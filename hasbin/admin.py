from django.contrib import admin
import hasbin.models as models


class DxGeneReferenceInline(admin.TabularInline):
    model = models.DxGeneReference


class DxGeneCommentInline(admin.TabularInline):
    model = models.DxGeneComment


class DxGeneAdmin(admin.ModelAdmin):
    inlines = [DxGeneReferenceInline, DxGeneCommentInline]


class BinnedGeneReferenceInline(admin.TabularInline):
    model = models.BinnedGeneReference


class BinnedGeneCommentInline(admin.TabularInline):
    model = models.BinnedGeneComment


class BinnedGeneAdmin(admin.ModelAdmin):
    inlines = [BinnedGeneReferenceInline, BinnedGeneCommentInline]


admin.site.register(models.DxGene, DxGeneAdmin)
admin.site.register(models.BinnedGene, BinnedGeneAdmin)

