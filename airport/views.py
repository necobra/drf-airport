from django.shortcuts import render
from rest_framework import viewsets

from airport import models


class AirportViewSet(viewsets.ModelViewSet):
    class Meta:
        model = models.Airport
        fields = ("id", "name", "closest_big_city")


class RouteViewSet(viewsets.ModelViewSet):
    class Meta:
        model = models.Route
        fields = ("id", "source", "destination", "distance")


class CrewViewSet(viewsets.ModelViewSet):
    class Meta:
        model = models.Crew
        fields = ("id", "first_name", "last_name")


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    class Meta:
        model = models.AirplaneType
        fields = ("id", "name")


class AirplaneViewSet(viewsets.ModelViewSet):
    class Meta:
        model = models.Airplane
        fields = (
            "id", "rows", "seats_in_row", "airplane_type", "capacity"
        )

class FlightViewSet(viewsets.ModelViewSet):
    class Meta:
        model = models.Flight
        fields = (
            "id", "route", "airplane", "departure_time", "arrival_time", "crew"
        )


class TicketViewSet(viewsets.ModelViewSet):
    class Meta:
        model = models.Ticket
        fields = (
            "row", "seat", "flight"
        )


class OrderViewSet(viewsets.ModelViewSet):
    class Meta:
        model = models.Order
        fields = (
            "created_at", "user"
        )
