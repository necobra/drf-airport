from time import sleep

from django.test import TestCase
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from airport.models import (
    Airport,
    Route,
    Crew,
    AirplaneType,
    Airplane,
    Flight,
    Ticket,
    Order,
)
from django.contrib.auth import get_user_model


class AirportModelTest(TestCase):

    def setUp(self):
        self.airport = Airport.objects.create(name="JFK", closest_big_city="New York")

    def test_str_method(self):
        self.assertEqual(str(self.airport), "JFK")

    def test_ordering(self):
        airport2 = Airport.objects.create(name="LAX", closest_big_city="Los Angeles")
        airports = Airport.objects.all()
        self.assertEqual(list(airports), [self.airport, airport2])


class RouteModelTest(TestCase):

    def setUp(self):
        self.source = Airport.objects.create(name="JFK", closest_big_city="New York")
        self.destination = Airport.objects.create(
            name="LAX", closest_big_city="Los Angeles"
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=4000
        )

    def test_str_method(self):
        self.assertEqual(str(self.route), "JFK-LAX")

    def test_ordering(self):
        route2 = Route.objects.create(
            source=self.destination, destination=self.source, distance=4000
        )
        routes = Route.objects.all()
        self.assertEqual(list(routes), [self.route, route2])


class CrewModelTest(TestCase):

    def setUp(self):
        self.crew = Crew.objects.create(first_name="John", last_name="Doe")

    def test_full_name_property(self):
        self.assertEqual(self.crew.full_name, "John Doe")

    def test_str_method(self):
        self.assertEqual(str(self.crew), "John Doe")


class AirplaneModelTest(TestCase):

    def setUp(self):
        self.airplane_type = AirplaneType.objects.create(name="Boeing 747")
        self.airplane = Airplane.objects.create(
            name="Airplane 1", rows=30, seats_in_row=6, airplane_type=self.airplane_type
        )

    def test_capacity_property(self):
        self.assertEqual(self.airplane.capacity, 180)

    def test_str_method(self):
        self.assertEqual(str(self.airplane), "Airplane 1")


class FlightModelTest(TestCase):

    def setUp(self):
        self.source = Airport.objects.create(name="JFK", closest_big_city="New York")
        self.destination = Airport.objects.create(
            name="LAX", closest_big_city="Los Angeles"
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=4000
        )
        self.airplane_type = AirplaneType.objects.create(name="Boeing 747")
        self.airplane = Airplane.objects.create(
            name="Airplane 1", rows=30, seats_in_row=6, airplane_type=self.airplane_type
        )
        self.crew_member = Crew.objects.create(first_name="John", last_name="Doe")
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=datetime.now(),
            arrival_time=datetime.now() + timedelta(hours=5),
        )
        self.flight.crew.add(self.crew_member)

    def test_str_method(self):
        self.assertEqual(str(self.flight), "Airplane 1 JFK-LAX")

    def test_clean_method(self):
        self.flight.arrival_time = self.flight.departure_time + timedelta(hours=1)
        self.flight.clean()

        self.flight.arrival_time = self.flight.departure_time - timedelta(hours=1)
        with self.assertRaises(ValidationError):
            self.flight.clean()


class TicketModelTest(TestCase):

    def setUp(self):
        self.source = Airport.objects.create(name="JFK", closest_big_city="New York")
        self.destination = Airport.objects.create(
            name="LAX", closest_big_city="Los Angeles"
        )
        self.route = Route.objects.create(
            source=self.source, destination=self.destination, distance=4000
        )
        self.airplane_type = AirplaneType.objects.create(name="Boeing 747")
        self.airplane = Airplane.objects.create(
            name="Airplane 1", rows=30, seats_in_row=6, airplane_type=self.airplane_type
        )
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=datetime.now(),
            arrival_time=datetime.now() + timedelta(hours=5),
        )
        self.user = get_user_model().objects.create_user(email="test@test.test")
        self.order = Order.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(
            row=10, seat=5, flight=self.flight, order=self.order
        )

    def test_str_method(self):
        self.assertEqual(str(self.ticket), f"{str(self.flight)} (row: 10, seat: 5)")

    def test_clean_method(self):
        self.ticket.clean()

        self.ticket.row = 35
        with self.assertRaises(ValidationError):
            self.ticket.clean()


class OrderModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(email="testuser@test.test")
        self.order = Order.objects.create(user=self.user)

    def test_str_method(self):
        self.assertEqual(str(self.order), str(self.order.created_at))
