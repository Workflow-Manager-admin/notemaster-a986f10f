from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .models import Note

class HealthTests(APITestCase):
    def test_health(self):
        url = reverse('Health')  # Make sure the URL is named
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"message": "Server is up!"})

class AuthAndNotesTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="password123")
        self.token = Token.objects.create(user=self.user)

    def test_register(self):
        url = reverse('register')
        data = {"username": "testuser", "password": "testpass999"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue("id" in response.data)

    def test_login(self):
        url = reverse('login')
        data = {"username": "alice", "password": "password123"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("token" in response.data)

    def test_note_crud(self):
        # Authenticate
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        # Create note
        create_url = reverse("note-list-create")
        note_data = {"title": "First Note", "content": "Contents..."}
        response = self.client.post(create_url, note_data)
        self.assertEqual(response.status_code, 201)
        note_id = response.data["id"]

        # Read note
        detail_url = reverse("note-detail", args=[note_id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "First Note")

        # Update note
        response = self.client.put(detail_url, {"title": "Updated", "content": "Changed"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Updated")

        # Delete note
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Note.objects.filter(id=note_id).exists())

    def test_note_search(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        Note.objects.create(title="Alpha note", content="Content1", owner=self.user)
        Note.objects.create(title="Beta", content="Searchable text", owner=self.user)
        url = reverse("note-list-create")
        response = self.client.get(url, {"search": "Alpha"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Alpha note")
