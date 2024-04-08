from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from nest.models import User


class UserAPITest(APITestCase):
    def test_get_user_list(self):
        url = reverse("user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_detail(self):
        user = User.objects.create(username="testuser", email="test@example.com")
        url = reverse("user-detail", kwargs={"pk": user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
