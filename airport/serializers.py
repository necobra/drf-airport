from django.db import transaction
from rest_framework import serializers
from rest_framework import exceptions

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
    airplane_capacity = serializers.IntegerField(
        source="airplane.capacity", read_only=True
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "airplane_capacity",
            "tickets_available",
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        models.Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            exceptions.ValidationError,
        )
        return data

    class Meta:
        model = models.Ticket
        fields = ("id", "row", "seat", "flight")


class TicketListSerializer(TicketSerializer):
    flight = FlightListSerializer(many=False, read_only=True)


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = models.Ticket
        fields = ("row", "seat")


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Crew
        fields = ("id", "first_name", "last_name", "flights")


class CrewListSerializer(CrewSerializer):
    flights = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = models.Crew
        fields = ("id", "first_name", "last_name", "flights")


class CrewShortSerializer(CrewSerializer):
    class Meta:
        model = models.Crew
        fields = ("id", "first_name", "last_name")


class FlightDetailSerializer(FlightSerializer):
    route = RouteListSerializer()
    airplane = AirplaneSerializer()
    crew = CrewShortSerializer(many=True)
    taken_places = TicketSeatsSerializer(source="tickets", many=True, read_only=True)

    class Meta:
        model = models.Flight
        fields = (
            "id",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "crew",
            "taken_places",
        )


class CrewDetailSerializer(CrewSerializer):
    flights = FlightListSerializer(read_only=True, many=True)

    class Meta:
        model = models.Crew
        fields = ("id", "first_name", "last_name", "flights")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AirplaneType
        fields = ("id", "name")


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = models.Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = models.Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                models.Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
