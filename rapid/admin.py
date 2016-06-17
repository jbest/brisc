from django.contrib import admin
from rapid.models import FolderType
from rapid.models import Group
from rapid.models import Family
from rapid.models import Genus
from rapid.models import Species
from rapid.models import Inventory
from rapid.models import Session
from rapid.models import TaxonSet


class SessionAdmin(admin.ModelAdmin):
    readonly_fields = ('startTime', 'endTime')  # Makes auto_add fields visible


# Below gets around problem of loading ALL taxa in the admin view
#http://stackoverflow.com/questions/12573659/a-lots-of-foreign-keys-django-admin
class TaxonSetAdmin(admin.ModelAdmin):
    raw_id_fields = ('family', 'genus', 'species', )
    readonly_fields = ('startTime', )  # Makes auto_add fields visible
# Options for registering all:
# https://github.com/Mimino666/django-admin-autoregister
# https://djangosnippets.org/snippets/2066/
# http://stackoverflow.com/questions/9443863/register-every-table-class-from-an-app-in-the-django-admin-page

admin.site.register(FolderType)
admin.site.register(Group)
admin.site.register(Family)
admin.site.register(Genus)
admin.site.register(Species)
admin.site.register(Inventory)
admin.site.register(Session, SessionAdmin)
admin.site.register(TaxonSet, TaxonSetAdmin)
