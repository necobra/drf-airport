from django.db.models import F, Count
from rest_framework import viewsets, filters, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from airport import models, serializers
from airport import filters as custom_filters


class AirportViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = models.Airport.objects.all()
    serializer_class = serializers.AirportSerializer
    search_fields = ["name", "closest_big_city"]


class RouteViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = models.Route.objects.select_related("source", "destination")
    serializer_class = serializers.RouteSerializer
    search_fields = ["source", "destination"]

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.RouteListSerializer
        if self.action == "retrieve":
            return serializers.RouteDetailSerializer
        return self.serializer_class


class CrewViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = models.Crew.objects.all()
    serializer_class = serializers.CrewSerializer
    search_fields = ["first_name", "last_name"]

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.CrewListSerializer
        if self.action == "retrieve":
            return serializers.CrewDetailSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset
        if self.action in ("retrieve", "list"):
            queryset = queryset.prefetch_related("flights")
        return queryset


class AirplaneTypeViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = models.AirplaneType.objects.all()
    serializer_class = serializers.AirplaneTypeSerializer
    search_fields = ["name"]


class AirplaneViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = models.Airplane.objects.select_related("airplane_type")
    serializer_class = serializers.AirplaneSerializer
    search_fields = ["name"]


class FlightViewSet(viewsets.ModelViewSet):
    queryset = (
        models.Flight.objects.select_related("airplane", "route")
        .prefetch_related("crew")
        .annotate(
            tickets_available=(
                F("airplane__rows") * F("airplane__seats_in_row") - Count("tickets")
            )
        )
    )
    serializer_class = serializers.FlightSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    filterset_class = custom_filters.FlightFilter
    search_fields = ["airplane", "route"]
    ordering_fields = ["route", "departure_time", "arrival_time"]

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.FlightListSerializer
        if self.action == "retrieve":
            return serializers.FlightDetailSerializer
        return self.serializer_class


class OrderViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = models.Order.objects.prefetch_related("tickets__flight")
    serializer_class = serializers.OrderSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return models.Order.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.OrderListSerializer

        return serializers.OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
