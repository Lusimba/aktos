from django.urls import path
from .views import ConsumerListAPIView, ConsumerDetailView

urlpatterns = [
    path("", ConsumerListAPIView.as_view(), name="consumer-list"),
    path("/<int:pk>", ConsumerDetailView.as_view(), name="consumer-detail"),
]
