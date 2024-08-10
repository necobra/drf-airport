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


class RouteListSerializer(RouteSerializer):
    source = serializers.CharField(
        max_length=255,
        source="source.name",
    )
    destination = serializers.CharField(
        max_length=255,
        source="destination.name",
    )

    class Meta:
        model = models.Route
        fields = ("id", "source", "destination", "distance")


class RouteDetailSerializer(RouteSerializer):
    source = AirportSerializer()
    destination = AirportSerializer()

    class Meta:
        model = models.Route
        fields = ("id", "source", "destination", "distance")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type", "capacity")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")


class FlightListSerializer(FlightSerializer):
    route = serializers.StringRelatedField()
    airplane = serializers.CharField(source="airplane.name")

    class Meta:
        model = models.Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time")


class FlightDetailSerializer(FlightSerializer):
    route = RouteListSerializer()
    airplane = AirplaneSerializer()
    crew = serializers.StringRelatedField(many=True)

    class Meta:
        model = models.Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Crew
        fields = ("id", "first_name", "last_name", "flights")


class CrewListSerializer(CrewSerializer):
    flights = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Crew
        fields = ("id", "first_name", "last_name", "flights")


class CrewDetailSerializer(CrewSerializer):
    flights = FlightListSerializer(read_only=True, many=True)

    class Meta:
        model = models.Crew
        fields = ("id", "first_name", "last_name", "flights")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AirplaneType
        fields = ("id", "name")


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Ticket
        fields = ("row", "seat", "flight")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Order
        fields = ("created_at", "user")
