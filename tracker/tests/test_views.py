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
        assert "unit" in entry
        assert entry["unit"] == "kg"  # default unit
        assert "timestamp" in entry
        # Should be ISO-8601 string
        assert isinstance(entry["timestamp"], str)
        assert len(entry["timestamp"]) > 0


@pytest.mark.django_db
def test_index_view_create_entry_different_units(client, django_user_model):
    """
    test that a weight entry can be created with different units (kg or lb).
    """
    user = django_user_model.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")

    # 1. Create entry with default unit (kg) by omitting unit or using kg
    response = client.post(
        reverse("index"),
        {"weight": "82.50", "unit": "kg", "timestamp": timezone.now().strftime("%Y-%m-%dT%H:%M:%S")},
    )
    assert response.status_code == 302  # redirects on success
    assert WeightEntry.objects.filter(user=user, weight="82.50", unit="kg").exists()

    # 2. Create entry with lb unit
    response = client.post(
        reverse("index"),
        {"weight": "180.50", "unit": "lb", "timestamp": timezone.now().strftime("%Y-%m-%dT%H:%M:%S")},
    )
    assert response.status_code == 302
    assert WeightEntry.objects.filter(user=user, weight="180.50", unit="lb").exists()


@pytest.mark.django_db
def test_export_entries_csv_contains_unit(client, django_user_model):
    """
    test that CSV export includes timestamp, weight, and unit.
    """
    user = django_user_model.objects.create_user(username="testuser", password="password")
    client.login(username="testuser", password="password")

    WeightEntry.objects.create(user=user, weight=75.5, unit="kg", timestamp=timezone.now())
    WeightEntry.objects.create(user=user, weight=165.0, unit="lb", timestamp=timezone.now())

    response = client.get(reverse("export_entries_csv"))
    assert response.status_code == 200
    assert response["Content-Type"] == "text/csv"

    content = response.content.decode("utf-8")
    lines = content.strip().split("\r\n")
    
    # Check CSV header
    assert lines[0] == "timestamp,weight,unit"
    assert len(lines) == 3
    assert "75.50,kg" in lines[1] or "75.50,kg" in lines[2]
    assert "165.00,lb" in lines[1] or "165.00,lb" in lines[2]
