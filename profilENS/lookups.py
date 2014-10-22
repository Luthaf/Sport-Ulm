from selectable.registry import registry
from selectable.base import ModelLookup
from profilENS.models import User, Departement


class UserLookup(ModelLookup):
    model = User
    search_fields = ('first_name__icontains', 'last_name__icontains' )

registry.register(UserLookup)


class DepartementLookup(ModelLookup):
    model = Departement
    search_fields = ('name__icontains',)

registry.register(DepartementLookup)
