import django.db.models as models


class HugoGene(models.Model):
    hgnc_id = models.PositiveSmallIntegerField(primary_key=True)
    symbol = models.CharField(max_length=32, verbose_name='HUGO symbol',)
    name = models.CharField(max_length=180, verbose_name='HUGO name',)
    # TODO - really an enum
    status = models.CharField(max_length=20, verbose_name='HUGO status',)
    # TODO - really an enum
    locus_type = models.CharField(max_length=32, null=True,)
    # TODO - really an enum
    locus_group = models.CharField(max_length=32, null=True,)
    location = models.CharField(max_length=48, verbose_name='chromosomal location', null=True,)
    entrez_id = models.PositiveIntegerField(null=True,)
    #### Lists of items referenced here
    # alias_symbols
    # ccds_ids
    # gene_families
    # omim_ids
    # prev_symbols
    # pubmed_ids
    # refseq_accessions
    ### TODO -- alt_ids as a synthesized list?

    def __str__(self):
        return "%s (%s)" % (self.symbol, self.name)


def make_hugo_list_field(field_name, field, field_plural=None):
    '''Gnarly class factory for many one-to-many tables'''

    class_name = 'Hugo' + ''.join([x.title() for x in field_name.split('_')])
    globals()[class_name] = type(class_name, (models.Model,), {
        field_name: field,
        'hugo_gene': models.ForeignKey(
            HugoGene,
            related_name=field_name + 's' if field_plural is None else field_plural,),
        '__module__': __name__,
        '__str__': lambda(self): str(self.__dict__[field_name]),
    },)

make_hugo_list_field('alias_symbol', models.CharField(max_length=32,),)
make_hugo_list_field('ccds_id', models.CharField(max_length=16,),)
make_hugo_list_field('gene_family', models.CharField(max_length=128,), 'gene_families',)
make_hugo_list_field('omim_id', models.PositiveIntegerField(verbose_name="OMIM ID",),)
make_hugo_list_field('prev_symbol', models.CharField(max_length=32, verbose_name='Previous Symbol'),)
make_hugo_list_field('pubmed_id', models.PositiveIntegerField(verbose_name="Pubmed ID",),)
make_hugo_list_field('refseq_accession', models.CharField(max_length=32,),)


class DxList(models.Model):
    name = models.CharField(max_length=64)
    official = models.BooleanField()
    last_update = models.DateTimeField(auto_now=True)
    #last_update_by = models.ForeignKey(Users)


class DxGene(models.Model):
    TIER_CHOICES = list(enumerate((
        'Do not include (0)',
        'Diagnostic, high-priority (1)',
        'Diagnostic, low-priority (2)',
        'Research use only (3)',
    )))
    gene = models.CharField(max_length=32)  # TODO- maybe enforce as ForeignKey to HugoGene vs. allowing/showing mismatched data
    phenotype = models.CharField(max_length=64)
    tier = models.PositiveSmallIntegerField(choices=TIER_CHOICES, null=True)
    syndromic = models.NullBooleanField()
    last_update = models.DateTimeField(auto_now=True, editable=False,)
    #last_update_by = models.ForeignKey(Users)
    dxlist = models.ForeignKey(DxList, related_name='gene_phenotype_pairs')


class DxGeneComment(models.Model):
    dx_gene = models.ForeignKey(DxGene, related_name="comments")
    comment = models.TextField()
    when = models.DateTimeField(auto_now=True, editable=False,)
    #user = models.ForeignKey(Users)


class DxGeneReference(models.Model):
    dx_gene = models.ForeignKey(DxGene, related_name="references")
    reference = models.TextField()
