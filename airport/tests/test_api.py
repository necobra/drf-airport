from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from airport.models import Airport, Route, Crew, AirplaneType, Airplane, Flight, Order

AIRPORT_URL = reverse("airport:airport-list")
ROUTE_URL = reverse("airport:route-list")
CREW_URL = reverse("airport:crew-list")
AIRPLANE_TYPE_URL = reverse("airport:airplanetype-list")
AIRPLANE_URL = reverse("airport:airplane-list")
FLIGHT_URL = reverse("airport:flight-list")
ORDER_URL = reverse("airport:order-list")


def sample_airport(**params):
    defaults = {"name": "Sample Airport", "closest_big_city": "Sample City"}
    defaults.update(params)
    return Airport.objects.create(**defaults)


def sample_route(source=None, destination=None, **params):
    source = source or sample_airport(name="Source Airport")
    destination = destination or sample_airport(name="Destination Airport")
    defaults = {"source": source, "destination": destination, "distance": 100}
    defaults.update(params)
    return Route.objects.create(**defaults)


def sample_crew(**params):
    defaults = {"first_name": "John", "last_name": "Doe"}
    defaults.update(params)
    return Crew.objects.create(**defaults)


def sample_airplane_type(**params):
    defaults = {"name": "Sample Type"}
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(airplane_type=None, **params):
    airplane_type = airplane_type or sample_airplane_type()
    defaults = {
        "name": "Sample Airplane",
        "rows": 10,
        "seats_in_row": 6,
        "airplane_type": airplane_type,
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


def sample_flight(route=None, airplane=None, **params):
    route = route or sample_route()
    airplane = airplane or sample_airplane()
    defaults = {
        "route": route,
        "airplane": airplane,
        "departure_time": "2024-08-12T10:00:00Z",
        "arrival_time": "2024-08-12T12:00:00Z",
    }
    defaults.update(params)
    return Flight.objects.create(**defaults)


class AirportViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_list_airports(self):
        sample_airport()
        sample_airport(name="Another Airport")
        res = self.client.get(AIRPORT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.assertEqual(len(res.data["results"]), 2)

    def test_create_airport(self):
        payload = {"name": "New Airport", "closest_big_city": "New City"}
        res = self.client.post(AIRPORT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Airport.objects.count(), 1)
        self.assertEqual(Airport.objects.get().name, "New Airport")


class RouteViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_list_routes(self):
        route = sample_route()
        res = self.client.get(ROUTE_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["results"][0]["id"], route.id)

    def test_create_route(self):
        source = sample_airport(name="Source Airport")
        destination = sample_airport(name="Destination Airport")
        payload = {"source": source.id, "destination": destination.id, "distance": 500}
        res = self.client.post(ROUTE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Route.objects.count(), 1)
        self.assertEqual(Route.objects.get().distance, 500)


class FlightViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_list_flights(self):
        flight = sample_flight()
        res = self.client.get(FLIGHT_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["results"][0]["id"], flight.id)

    def test_create_flight(self):
        route = sample_route()
        airplane = sample_airplane()
        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": "2024-08-12T10:00:00Z",
            "arrival_time": "2024-08-12T12:00:00Z",
        }
        res = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flight.objects.count(), 1)
        self.assertEqual(Flight.objects.get().route, route)


class OrderViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)

    def test_list_orders(self):
        order = Order.objects.create(user=self.user)
        res = self.client.get(ORDER_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data["results"]), 1)
        self.assertEqual(res.data["results"][0]["id"], order.id)

    def test_create_order(self):
        flight = sample_flight()
        payload = {"tickets": [{"row": 1, "seat": 1, "flight": flight.id}]}
        res = self.client.post(ORDER_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().tickets.count(), 1)
