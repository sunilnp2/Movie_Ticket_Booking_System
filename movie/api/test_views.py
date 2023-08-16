# import pytest
# from django.urls import reverse
# from rest_framework.test import APIClient
# from rest_framework import status

# @pytest.fixture
# def api_client():
#     return APIClient()

# def test_list_movies(api_client):
#     url = reverse('movie_list')  # Replace with your actual API endpoint URL
#     response = api_client.get(url)
#     assert response.status_code == status.HTTP_200_OK
