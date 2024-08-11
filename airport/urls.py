from rest_framework.routers import DefaultRouter

from airport import views


router = DefaultRouter()
router.register("orders", views.OrderViewSet)
router.register("crew", views.CrewViewSet)
router.register("airplane_types", views.AirplaneTypeViewSet)
router.register("airplanes", views.AirplaneViewSet)
router.register("airports", views.AirportViewSet)
router.register("flights", views.FlightViewSet)
router.register("routes", views.RouteViewSet)


urlpatterns = router.urls

app_name = "airport"
