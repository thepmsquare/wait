"""
tests for the tracker app views.
"""

import pytest
from django.urls import reverse


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
