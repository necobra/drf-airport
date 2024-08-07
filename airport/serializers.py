from rest_framework import serializers

from airport import models


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Route
        fields = ("id", "source", "destination", "distance")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Crew
        fields = ("id", "first_name", "last_name")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Airplane
        fields = (
            "id", "rows", "seats_in_row", "airplane_type", "capacity"
        )

class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Flight
        fields = (
            "id", "route", "airplane", "departure_time", "arrival_time", "crew"
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = (
            "row", "seat", "flight"
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = (
            "created_at", "user"
        )
