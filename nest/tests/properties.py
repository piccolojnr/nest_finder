from django.test import TestCase
from nest.models import (
    Address,
    ContactInformation,
    Property,
    User,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class PropertyAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.address = Address.objects.create(
            street="123 Main St", city="City", state="State", zipcode="12345"
        )
        self.contact_info = ContactInformation.objects.create(
            phone="123-456-7890", email="test@example.com", address=self.address
        )
        self.user = User.objects.create(
            username="test_user",
            email="user@example.com",
            profile_picture="http://example.com/profile.jpg",
            contact_information=self.contact_info,
            role="user",
        )
        self.property1 = Property.objects.create(
            user=self.user,
            title="House 1",
            description="Description 1",
            price=100000,
            type="house",
            address=self.address,
            latitude=1,
            longitude=2,
            images=["http://example.com/image1.jpg", "http://example.com/image2.jpg"],
        )
        self.property2 = Property.objects.create(
            user=self.user,
            title="House 2",
            description="Description 2",
            price=200000,
            type="house",
            address=self.address,
            latitude=1,
            longitude=2,
            images=["http://example.com/image1.jpg", "http://example.com/image2.jpg"],
        )

    def test_get_property_list(self):
        response = self.client.get(reverse("property-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_property_detail(self):
        response = self.client.get(reverse("property-detail", args=[self.property1.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "House 1")

    def test_create_property(self):
        data = {
            "user": self.user.id,
            "title": "New House",
            "description": "New Description",
            "price": 300000,
            "type": "house",
            "address": self.address.id,
            "latitude": 1,
            "longitude": 2,
            "status": "for_rent",
            "images": [
                "http://example.com/image1.jpg",
                "http://example.com/image2.jpg",
            ],
        }
        response = self.client.post(reverse("property-list"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 3)
        self.assertEqual(
            Property.objects.get(id=response.data["id"]).title, "New House"
        )

    def test_property_list_pagiantion(self):
        for i in range(10):
            Property.objects.create(
                user=self.user,
                title=f"House {i+1}",
                description=f"Description {i+1}",
                price=100000,
                type="house",
                address=self.address,
                latitude=1,
                longitude=2,
                images=[
                    "http://example.com/image1.jpg",
                    "http://example.com/image2.jpg",
                ],
            )

        response = self.client.get(
            reverse("property-list"), {"page": 1, "page_size": 5}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        response = self.client.get(
            reverse("property-list"), {"page": 2, "page_size": 5}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)

        response = self.client.get(
            reverse("property-list"), {"page": 3, "page_size": 5}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        response = self.client.get(
            reverse("property-list"), {"page": 4, "page_size": 5}
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_property(self):
        data = {
            "user": self.user.id,
            "title": "Updated House",
            "description": "Updated Description",
            "price": 300000,
            "type": "house",
            "address": self.address.id,
            "latitude": 1,
            "longitude": 2,
            "status": "for_rent",
            "images": [
                "http://example.com/image1.jpg",
                "http://example.com/image2.jpg",
            ],
        }
        response = self.client.put(
            reverse("property-detail", args=[self.property1.id]), data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Property.objects.count(), 2)
        self.assertEqual(
            Property.objects.get(id=response.data["id"]).title, "Updated House"
        )

    def test_delete_property(self):
        response = self.client.delete(
            reverse("property-detail", args=[self.property1.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Property.objects.count(), 1)
        self.assertEqual(Property.objects.get(id=self.property2.id).title, "House 2")
