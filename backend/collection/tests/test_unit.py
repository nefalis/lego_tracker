import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from collection.models import LegoSet


@pytest.mark.django_db
class TestLegoSetViewSet:

    def setup_method(self):
        """Configuration avant chaque test"""
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
            )
        self.lego_set = LegoSet.objects.create(
            name="Millennium Falcon", user=self.user, lego_id=75192
            )

    def test_list_unauthorized(self):
        """Test : un utilisateur non authentifié ne peut pas accéder aux LEGO sets"""
        response = self.client.get("/api/legosets/")
        assert response.status_code == 403

    def test_list_authorized(self):
        """Test : un utilisateur authentifié peut récupérer ses LEGO sets"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/legosets/")
        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["name"] == "Millennium Falcon"

    def test_create_legoset(self):
        """Test : un utilisateur authentifié peut créer un LEGO set"""
        self.client.force_authenticate(user=self.user)
        data = {"name": "Fondcombe", "lego_id": 10316, "user": self.user.id}
        response = self.client.post("/api/legosets/", data)
        assert response.status_code == 201
        assert LegoSet.objects.count() == 2
