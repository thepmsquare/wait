import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from tracker.models import WeightEntry


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_api_token_retrieval(api_client, django_user_model):
    """
    Test retrieving an authentication token.
    """
    user = django_user_model.objects.create_user(username="apiuser", password="password")

    url = reverse("api_token_auth")
    response = api_client.post(url, {"username": "apiuser", "password": "password"})

    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.data

    # Verify the token is indeed saved in database
    token = Token.objects.get(user=user)
    assert response.data["token"] == token.key


@pytest.mark.django_db
def test_api_unauthenticated_access(api_client):
    """
    Test that API endpoints are protected.
    """
    url = reverse("weightentry-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_api_crud_operations(api_client, django_user_model):
    """
    Test CRUD operations on weight entries via API.
    """
    user = django_user_model.objects.create_user(username="apiuser", password="password")
    token = Token.objects.create(user=user)
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    # 1. Create weight entry
    url = reverse("weightentry-list")
    data = {"weight": "78.50"}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["weight"] == "78.50"
    assert response.data["user"] == "apiuser"

    entry_id = response.data["id"]

    # 2. List weight entries
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == entry_id

    # 3. Retrieve weight entry
    detail_url = reverse("weightentry-detail", kwargs={"pk": entry_id})
    response = api_client.get(detail_url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["weight"] == "78.50"

    # 4. Update weight entry
    update_data = {"weight": "79.00"}
    response = api_client.put(detail_url, update_data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["weight"] == "79.00"

    # 5. Delete weight entry
    response = api_client.delete(detail_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert WeightEntry.objects.filter(id=entry_id).count() == 0


@pytest.mark.django_db
def test_api_user_isolation(api_client, django_user_model):
    """
    Test that users cannot see or modify other users' entries.
    """
    user1 = django_user_model.objects.create_user(username="user1", password="password")
    user2 = django_user_model.objects.create_user(username="user2", password="password")

    token1 = Token.objects.create(user=user1)
    token2 = Token.objects.create(user=user2)

    # Create entry for user1
    entry = WeightEntry.objects.create(user=user1, weight=80.0)

    # Authenticate as user2
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token2.key}")

    # Try to list (should be empty for user2)
    url = reverse("weightentry-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0

    # Try to retrieve user1's entry (should return 404)
    detail_url = reverse("weightentry-detail", kwargs={"pk": entry.id})
    response = api_client.get(detail_url)
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Try to update user1's entry (should return 404)
    response = api_client.put(detail_url, {"weight": "85.00"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

    # Try to delete user1's entry (should return 404)
    response = api_client.delete(detail_url)
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_api_cors_headers(api_client):
    """
    Test that CORS headers are present on API responses.
    """
    url = reverse("weightentry-list")
    response = api_client.get(url, HTTP_ORIGIN="http://localhost:3000")

    # Since CORS_ALLOW_ALL_ORIGINS = True (due to DEBUG=True in test environment)
    # The Access-Control-Allow-Origin header should be present and allow the origin.
    assert "access-control-allow-origin" in response
    assert response["access-control-allow-origin"] == "*"


@pytest.mark.django_db
def test_swagger_endpoints_accessible(api_client):
    """
    Test that schema, swagger-ui, and redoc endpoints are accessible.
    """
    schema_url = reverse("schema")
    swagger_url = reverse("swagger-ui")
    redoc_url = reverse("redoc")

    assert api_client.get(schema_url).status_code == status.HTTP_200_OK
    assert api_client.get(swagger_url).status_code == status.HTTP_200_OK
    assert api_client.get(redoc_url).status_code == status.HTTP_200_OK

