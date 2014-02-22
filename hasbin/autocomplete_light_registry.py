import autocomplete_light
from .models import HugoGene

autocomplete_light.register(HugoGene,
    search_fields = ('^symbol', ),
    autocomplete_js_attributes = {'placeholder': 'HUGO gene symbol?', },
)
