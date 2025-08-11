from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a user and get token (if using token auth)
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client = APIClient()
        self.client.login(username='testuser', password='password123')  # Or use token auth if implemented
        
        # Sample book data
        self.book_data = {
            'title': 'Test Book',
            'author': 'Author A',
            'published_date': '2020-01-01',
            'isbn': '1234567890123',
            'price': 29.99
        }
        # Create a book instance to test update, delete, etc
        self.book = Book.objects.create(**self.book_data)

    def test_create_book(self):
        url = reverse('book-list')  # Adjust name according to your router/namespaces
        data = {
            'title': 'New Book',
            'author': 'Author B',
            'published_date': '2021-05-05',
            'isbn': '9876543210987',
            'price': 19.99
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(response.data['title'], data['title'])

    def test_get_book_list(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_update_book(self):
        url = reverse('book-detail', args=[self.book.id])
        data = {'title': 'Updated Book'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, data['title'])

    def test_delete_book(self):
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())

    def test_filter_books_by_author(self):
        url = reverse('book-list') + '?author=Author A'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for book in response.data:
            self.assertEqual(book['author'], 'Author A')

    def test_permission_denied_for_unauthenticated(self):
        self.client.logout()
        url = reverse('book-list')
        response = self.client.post(url, self.book_data, format='json')
        self.assertIn(response.status_code, [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN])
