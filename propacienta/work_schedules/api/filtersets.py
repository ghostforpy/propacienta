from django_filters import DateFromToRangeFilter
from django_filters.rest_framework import FilterSet

from ..models import WorkDay


class DateRangeFilterSet(FilterSet):
    date_range = DateFromToRangeFilter(label="Диапазон дат")

    class Meta:
        model = WorkDay
        fields = ["date_range", "doctor", "hospital", "date"]
