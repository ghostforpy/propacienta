from django_filters import BooleanFilter, DateTimeFromToRangeFilter
from django_filters.rest_framework import FilterSet

from ..models import AppointmentOrder


class DateTimeRangeFilterSet(FilterSet):
    dt = DateTimeFromToRangeFilter(label="Диапазон временных штампов")

    class Meta:
        model = AppointmentOrder
        fields = ["dt"]
