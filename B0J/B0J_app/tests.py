from django.test import TestCase
from django.urls import reverse

class B0JAppTests(TestCase):
    def test_index_view(self):
        """Тест главной страницы"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_about_view(self):
        """Тест страницы о компании"""
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')
    
    def test_drivers_view(self):
        """Тест страницы водителей"""
        response = self.client.get('/drivers/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'drivers.html')
    
    def test_contacts_view(self):
        """Тест страницы контактов"""
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts.html')