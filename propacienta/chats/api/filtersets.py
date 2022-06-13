from django_filters import BooleanFilter, DateTimeFromToRangeFilter
from django_filters.rest_framework import FilterSet

from ..models import DialogMessage


class DialogMessageFilterSet(FilterSet):

    class Meta:
        model = DialogMessage
        fields = ["dialog"]
