from django.forms import ModelForm
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from rapid.models import Inventory, Session, TaxonSet


class InventoryForm(ModelForm):
# see https://docs.djangoproject.com/en/1.7/topics/forms/#building-a-form-in-django

    class Meta:
        model = Inventory
        fields = ['description', ]


class SessionForm(ModelForm):
# see https://docs.djangoproject.com/en/1.7/topics/forms/#building-a-form-in-django

# http://stackoverflow.com/questions/1697702/how-to-pass-initial-parameter-to-djangos-modelform-instance

    def __init__(self, *args, **kwargs):
        print kwargs
        inventory = kwargs.pop('inventory')
        super(SessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        # Inventory is set prior to session creation
        fields = ['recorder', 'counter']


class SessionFormOLD(ModelForm):
# see https://docs.djangoproject.com/en/1.7/topics/forms/#building-a-form-in-django

    class Meta:
        model = Session
        fields = ['inventory', 'recorder', 'counter']


class TaxonSetForm(ModelForm):
# see https://docs.djangoproject.com/en/1.7/topics/forms/#building-a-form-in-django
    """
    def __init__(self, *args, **kwargs):
        super(TaxonSetForm, self).__init__(*args, **kwargs)
        self.fields['session'] = '1'
        """

    class Meta:
        model = TaxonSet
        #fields = ['group', 'family', 'genus', 'species', 'count', 'container']
        fields = ['group', 'family', 'genus', 'species', 'count']
