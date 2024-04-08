# urls.py
from django.urls import path
from .views import (
    PropertyListAPIView,
    PropertyDetailAPIView,
    UserListAPIView,
    UserDetailAPIView,
)

urlpatterns = [
    path("properties/", PropertyListAPIView.as_view(), name="property-list"),
    path(
        "properties/<int:pk>/",
        PropertyDetailAPIView.as_view(),
        name="property-detail",
    ),
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
]
