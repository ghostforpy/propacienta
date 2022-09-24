from django.db.models import Q
from django_filters import DateTimeFromToRangeFilter, NumberFilter
from django_filters.rest_framework import FilterSet

from ..models import WebDial


class DateTimeRangeFilterSet(FilterSet):
    start_webdial = DateTimeFromToRangeFilter()
    opponent = NumberFilter(method='filter_opponent')

    class Meta:
        model = WebDial
        fields = ["start_webdial", "opponent", "webdial_happen"]

    def filter_opponent(self, queryset, name, value):
        return queryset.filter(
            Q(initiator__id=value) | Q(opponent__id=value)
        )
