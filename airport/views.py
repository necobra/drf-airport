from django.shortcuts import render
from rest_framework import viewsets

from airport import models, serializers


class AirportViewSet(viewsets.ModelViewSet):
    queryset = models.Airport.objects.all()
    serializer_class = serializers.AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = models.Route.objects.all()
    serializer_class = serializers.RouteSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = models.Crew.objects.all()
    serializer_class = serializers.CrewSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = models.AirplaneType.objects.all()
    serializer_class = serializers.AirplaneTypeSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = models.Airplane.objects.all()
    serializer_class = serializers.AirplaneSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = models.Flight.objects.all()
    serializer_class = serializers.FlightSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = models.Ticket.objects.all()
    serializer_class = serializers.TicketSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
