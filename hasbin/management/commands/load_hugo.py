from django.core.management.base import BaseCommand
from django.db import transaction
import hasbin.models as model
import gzip
import json


def auto_gunzip(f):
    if f.endswith('.gz'):
        return gzip.open(f)
    else:
        return open(f)


def int_or_none(x):
    try:
        return int(x)
    except ValueError:
        return None


class Command(BaseCommand):
    args = '<hgnc_json_file>'
    help = 'populate the HugoGene table from hugo json file (like returned by the REST server)'

    @transaction.atomic()
    def handle(self, *args, **options):
        with auto_gunzip(args[0]) as inf:
            data = json.load(inf, encoding='latin1')
        try:
            print "found %d items" % data['response']['numFound']
        except KeyError:
            print "unable to parse hgnc json file"
            raise
        for d in data['response']['docs']:
            init_data = dict(((k, d[k]) for k in model.HugoGene._meta.get_all_field_names() if k in d))
            g = model.HugoGene.objects.create(**init_data)
            g.alias_symbols = [model.HugoAliasSymbol(alias_symbol=x) for x in d.get('alias_symbol', ())]
            g.ccds_ids = [model.HugoCcdsId(ccds_id=x) for x in d.get('ccds_id', ())]
            g.gene_families = [model.HugoGeneFamily(gene_family=x) for x in d.get('gene_family', ())]
            g.omim_ids = [model.HugoOmimId(omim_id=x) for x in d.get('omim_id', ())]
            g.prev_symbols = [model.HugoPrevSymbol(prev_symbol=x) for x in d.get('prev_symbol', ())]
            g.pubmed_ids = [model.HugoPubmedId(pubmed_id=x) for x in d.get('pubmed_id', ())]
            g.refseq_accessions = [model.HugoRefseqAccession(refseq_accession=x) for x in d.get('refseq_accession', ())]
