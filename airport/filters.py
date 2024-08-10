from django_filters import rest_framework as filters
from airport import models


class FlightFilter(filters.FilterSet):
    departure_time = filters.DateTimeFromToRangeFilter(field_name="departure_time")
    arrival_time = filters.DateTimeFromToRangeFilter(field_name="arrival_time")

    class Meta:
        model = models.Flight
        fields = ["route"]
