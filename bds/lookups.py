from selectable.registry import registry
from selectable.base import ModelLookup
from bds.models import Sportif, Event


class SportifLookup(ModelLookup):
    model = Sportif
    search_fields = ('user__first_name__icontains',
                     'user__last_name__icontains'
                     )

registry.register(SportifLookup)


class EventLookup(ModelLookup):
    model = Event
    search_fields = ('name__icontains',
                     )

registry.register(EventLookup)
