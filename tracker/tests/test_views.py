import pytest
from django.urls import reverse
from django.utils import timezone
from tracker.models import WeightEntry


@pytest.mark.django_db
def test_index_view_authenticated(client, django_user_model):
    """
    test that the index view is accessible when authenticated.
    """
    django_user_model.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")
    response = client.get(reverse("index"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_index_view_unauthenticated(client):
    """
    test that the index view redirects to login when not authenticated.
    """
    response = client.get(reverse("index"))
    assert response.status_code == 302  # should redirect to login


@pytest.mark.django_db
def test_index_view_context_all_entries(client, django_user_model):
    """
    test that the index view contains all user weight entries serialized correctly.
    """
    user = django_user_model.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")

    # Create 3 weight entries for this user
    WeightEntry.objects.create(user=user, weight=75.5, timestamp=timezone.now())
    WeightEntry.objects.create(user=user, weight=76.2, timestamp=timezone.now())
    WeightEntry.objects.create(user=user, weight=74.8, timestamp=timezone.now())

    response = client.get(reverse("index"))
    assert response.status_code == 200
    
    assert "all_entries" in response.context
    all_entries = response.context["all_entries"]
    assert len(all_entries) == 3
    
    # Check structure
    for entry in all_entries:
        assert isinstance(entry["weight"], float)
        assert "timestamp" in entry
        # Should be ISO-8601 string
        assert isinstance(entry["timestamp"], str)
        assert len(entry["timestamp"]) > 0
