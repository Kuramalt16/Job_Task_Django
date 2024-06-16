from django.test import TestCase
from django.urls import resolve, reverse
from Company.views import (Company_home, Company_list,
                           New_Company, View_Company,
                           Delete_Company, Update_Company,
                           Export_company)


class test_urls(TestCase):

    def test_company_home_company_url_is_resolved(self):
        url = reverse("companies:company_home")
        self.assertEqual(resolve(url).func, Company_home)

    def test_company_list_url_is_resolved(self):
        url = reverse("companies:campanies_list")
        self.assertEqual(resolve(url).func, Company_list)

    def test_new_company_url_is_resolved(self):
        url = reverse("companies:new_company")
        self.assertEqual(resolve(url).func, New_Company)

    def test_view_company_url_is_resolved(self):
        url = reverse("companies:view_company", args=['some-slug'])
        self.assertEqual(resolve(url).func, View_Company)

    def test_delete_company_url_is_resolved(self):
        url = reverse("companies:delete_company", args=['some-slug'])
        self.assertEqual(resolve(url).func, Delete_Company)

    def test_update_company_url_is_resolved(self):
        url = reverse("companies:update_company", args=['some-slug'])
        self.assertEqual(resolve(url).func, Update_Company)

    def test_export_url_is_resolved(self):
        url = reverse("companies:single_export", args=['some-slug'])
        self.assertEqual(resolve(url).func, Export_company)
