from django.shortcuts import render
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from airport import models, serializers
from airport import filters as custom_filters


class AirportViewSet(viewsets.ModelViewSet):
    queryset = models.Airport.objects.all()
    serializer_class = serializers.AirportSerializer
    search_fields = ["name", "closest_big_city"]


class RouteViewSet(viewsets.ModelViewSet):
    queryset = models.Route.objects.all()
    serializer_class = serializers.RouteSerializer
    search_fields = ["source", "destination"]

    def get_serializer_class(self):
        if self.action == "list":
            return serializers.RouteListSerializer
        if self.action == "retrieve":
            return serializers.RouteDetailSerializer
        return self.serializer_class


class CrewViewSet(viewsets.ModelViewSet):
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
        if self.action == "retrieve":
            queryset = queryset.prefetch_related("flights")
        return queryset


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = models.AirplaneType.objects.all()
    serializer_class = serializers.AirplaneTypeSerializer
    search_fields = ["name"]


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = models.Airplane.objects.all()
    serializer_class = serializers.AirplaneSerializer
    search_fields = ["name"]


class FlightViewSet(viewsets.ModelViewSet):
    queryset = models.Flight.objects.all()
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


class TicketViewSet(viewsets.ModelViewSet):
    queryset = models.Ticket.objects.all()
    serializer_class = serializers.TicketSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
