import django.db.models as models
from simple_history.models import HistoricalRecords


class HugoGene(models.Model):
    hgnc_id = models.PositiveSmallIntegerField(unique=True,)
    symbol = models.CharField(max_length=32, verbose_name='HUGO symbol', primary_key=True,)
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
    description = models.TextField(blank=True, default='')
    version = models.CharField(max_length=16)
    official = models.BooleanField(default=False)
    history = HistoricalRecords()


class DxGene(models.Model):
    TIER_CHOICES = list(enumerate((
        'Do not include (0)',
        'Diagnostic, high-priority (1)',
        'Diagnostic, low-priority (2)',
        'Research use only (3)',
    )))
    INHERITANCE_CHOICES = (
        ('AD', 'Autosomal dominant'),
        ('AR', 'Autosomal recessive'),
        ('XD', 'X-linked dominant'),
        ('XR', 'X-linked recessive'),
        ('CX', 'Complex'),
    )
    symbol = models.CharField(max_length=32)
    hugo_gene = models.ForeignKey(HugoGene, related_name='dxgenes', null=True)
    phenotype = models.CharField(max_length=64)
    tier = models.PositiveSmallIntegerField(choices=TIER_CHOICES, null=True)
    syndromic = models.NullBooleanField()
    inheritance = models.CharField(max_length=3, null=True, choices=INHERITANCE_CHOICES)
    dxlist = models.ForeignKey(DxList, related_name='gene_phenotype_pairs')
    unique_together = ('dxlist', 'symbol', 'phenotype')
    history = HistoricalRecords()

    def __str__(self):
        return "%s : %s" % (str(self.gene), self.phenotype)


class DxGeneComment(models.Model):
    dx_gene = models.ForeignKey(DxGene, related_name="comments")
    comment = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        if len(self.comment) > 50:
            return self.comment[:50] + '...'
        else:
            return self.comment


class DxGeneReference(models.Model):
    dx_gene = models.ForeignKey(DxGene, related_name="references")
    reference = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        return reference


class BinnedGene(models.Model):
    LIKELIHOOD_CHOICES = list(enumerate((
        "<1% or unable to determine",
        "1-5%",
        "6-49%",
        ">50%"
        )))
    SEVERITY_CHOICES = list(enumerate((
        "Modest or no morbidity",
        "Serious morbidity",
        "Possible death",
        "Sudden death"
        )))
    ACCEPTABILITY_CHOICES = list(enumerate((
        "Onerous (e.g. prophylactic gastrectomy)",
        "Minimally acceptable (prophylactic surgery)",
        "Moderately acceptable (invasive screening, dietary restrictions)",
        "Highly acceptable (annual blood tests)"
        )))
    EFFICACY_CHOICES = list(enumerate((
        "Ineffective",
        "Minimally effective",
        "Modestly effective",
        "Highly effective"
        )))
    EVIDENCE_CHOICES = list(enumerate((
        "Controversial or poor evidence",
        "Minimal evidence",
        "Moderate evidence",
        "Substantial evidence"
        )))
    symbol = models.CharField(max_length=32)
    hugo_gene = models.ForeignKey(HugoGene, related_name='binned_genes', null=True)
    phenotype = models.CharField(max_length=64)
    outcome_of_interest = models.CharField(max_length=64,)
    likelihood_of_outcome = models.PositiveSmallIntegerField(choices=LIKELIHOOD_CHOICES, null=True,)
    severity_of_outcome = models.PositiveSmallIntegerField(choices=SEVERITY_CHOICES, null=True,)
    intervention = models.CharField(max_length=64,)
    acceptability_of_intervention = models.PositiveSmallIntegerField(choices=ACCEPTABILITY_CHOICES, null=True,)
    efficacy_of_intervention = models.PositiveSmallIntegerField(choices=EFFICACY_CHOICES, null=True,)
    evidence_base = models.PositiveSmallIntegerField(choices=EVIDENCE_CHOICES, null=True,)
    history = HistoricalRecords()

    def score(self):
        return sum([x or 0 for x in (self.likelihood_of_outcome, self.severity_of_outcome,
            self.acceptability_of_intervention, self.efficacy_of_intervention, self.evidence_base)])

    def __str__(self):
        return "%s : %s : %d" % (str(self.hugo_gene), self.phenotype, self.score())


class BinnedGeneReference(models.Model):
    binned_gene = models.ForeignKey(BinnedGene, related_name="references")
    reference = models.CharField(max_length=128)
    history = HistoricalRecords()

    def __str__(self):
        return self.reference


class BinnedGeneComment(models.Model):
    binned_gene = models.ForeignKey(BinnedGene, related_name="comments")
    comment = models.TextField()
    history = HistoricalRecords()

    def __str__(self):
        if len(self.comment) > 50:
            return self.comment[:50] + '...'
        else:
            return self.comment

