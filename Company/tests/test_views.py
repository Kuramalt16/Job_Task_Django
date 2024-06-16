from django.test import TestCase, Client
from django.urls import reverse
from Company.models import Companies
from unittest.mock import patch


class test_views(TestCase):

    def setUp(self):
        self.client = Client()
        self.chome_url = reverse('companies:company_home')
        self.clist_url = reverse('companies:campanies_list')
        self.cnew_url = reverse('companies:new_company')
        self.company_data = {'ticker': 'AAPL'}
        self.cview_url = reverse('companies:view_company', args=[self.company_data['ticker']])
        self.cdelete_url = reverse('companies:delete_company', args=[self.company_data['ticker']])
        self.cexport_url = reverse('companies:single_export', args=[self.company_data['ticker']])

    def test_company_home_GET(self):
        response = self.client.get(self.chome_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/company_home.html')

    def test_company_list_GET(self):
        response = self.client.get(self.clist_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/company_list.html')

    def test_new_company_GET(self):
        response = self.client.get(self.cnew_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/new_company.html')
        self.assertEqual(response.context['error'], 0)

    @patch('yfinance.Ticker')
    def test_new_company_POST(self, mock_ticker):
        mock_instance = mock_ticker.return_value
        mock_instance.info = {
            "longName": "Mock Company",
            "industry": "Mock Industry",
            "volume": 1000000,
            "open": 10,
            "previousClose": 10,
            "dayHigh": 10,
            "dayLow": 10
        }

        response = self.client.post(self.cnew_url, self.company_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Companies.objects.filter(company_symbol='AAPL').exists())
        company = Companies.objects.get(company_symbol='AAPL')
        self.assertEqual(company.company_name, 'Mock Company')
        company.delete()

    def test_new_company_POST_already_exists(self):
        Companies.objects.create(
            company_symbol='AAPL',
            company_name='Existing Company',
            company_industry='Existing Industry',
            company_volume=500000,
            company_open=10,
            company_close=10,
            company_high=10,
            company_low=10
        )

        response = self.client.post(self.cnew_url, self.company_data)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/new_company.html')
        self.assertEqual(response.context['error'], 1)
        self.assertEqual(response.context['ticker'], 'AAPL')
        company = Companies.objects.get(company_symbol='AAPL')
        company.delete()

    def test_new_company_POST_invalid_ticker(self):
        response = self.client.post(self.cnew_url, data={'ticker': 'INVALID'})
        # print("\n\n\n\n", "testing New Company INVALID \n\n\n\n")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/new_company.html')
        self.assertEqual(response.context['error'], 2)
        self.assertEqual(response.context['ticker'], 'INVALID')

    def test_view_company_GET(self):
        Companies.objects.create(
            company_symbol='AAPL',
            company_name='Existing Company',
            company_industry='Existing Industry',
            company_volume=500000,
            company_open=10,
            company_close=10,
            company_high=10,
            company_low=10
        )

        response = self.client.get(self.cview_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'company/view_company.html')

        company = Companies.objects.get(company_symbol='AAPL')
        company.delete()

    def test_view_company_POST_updates_db(self):
        company = Companies.objects.create(
            company_name='Test Company',
            company_symbol='AAPL',
            company_industry='Technology',
            company_volume=1000.0,
            company_open=10,
            company_close=10,
            company_high=10,
            company_low=10
        )

        updated_data = {
            'name': 'Updated Test Company',
            'industry': 'Updated Technology',
            'volume': 2000.0,
            'open': 10,
            'close': 10,
            'high': 10,
            'low': 10
        }

        response = self.client.post(self.cview_url, updated_data)

        company.refresh_from_db()

        self.assertEqual(company.company_name, updated_data['name'])
        self.assertEqual(company.company_industry, updated_data['industry'])
        self.assertEqual(company.company_volume, updated_data['volume'])
        self.assertEqual(response.status_code, 200)

        company.delete()

    def test_delete_company_POST(self):
        company = Companies.objects.create(
            company_name='Test Company',
            company_symbol='AAPL',
            company_industry='Technology',
            company_volume=1000.0,
            company_open=10,
            company_close=10,
            company_high=10,
            company_low=10
        )

        response = self.client.post(self.cdelete_url, {'company_symbol': 'AAPL'})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Companies.objects.filter(company_symbol='TEST').exists())

    def test_export_company_GET(self):
        Companies.objects.create(
            company_symbol='AAPL',
            company_name='Existing Company',
            company_industry='Existing Industry',
            company_volume=500000,
            company_open=10,
            company_close=10,
            company_high=10,
            company_low=10
        )
        response = self.client.get(self.cexport_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 0)

    def test_export_company_POST(self):
        company = Companies.objects.create(
            company_symbol='AAPL',
            company_name='Test Company',
            company_industry='Technology',
            company_volume=500000,
            company_open=10,
            company_close=10,
            company_high=10,
            company_low=10
        )
        post_data = {
            'sdate': "2020-02-07",
            'edate': "2020-02-08"
        }

        response = self.client.post(self.cexport_url, post_data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.get('Content-Disposition'), 'attachment; filename="AAPL.csv"')

        content = response.content.decode('utf-8').splitlines()

        self.assertEqual(len(content), 4)  # checks if the amount of rows generated is equal to 4
        self.assertTrue(content[1].startswith('AAPL,Test Company,Technology'))
        self.assertTrue(content[3].startswith('2020-02-07 00:00:00-05:00'))

        company.delete()

    def test_export_company_POST_invalid_date(self):
        company = Companies.objects.create(
            company_name='Test Company',
            company_symbol='AAPL',
            company_industry='Technology',
            company_volume=117684000,
            company_open=10,
            company_close=10,
            company_high=10,
            company_low=10
        )
        post_data = {
            'sdate': "2020-02-09",
            'edate': "2020-02-08"
        }

        response = self.client.post(self.cexport_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 1)  # testing for error (start date is after end date)

        post_data = {
            'sdate': "2019-13-09",
            'edate': "2020-02-01"
        }

        response = self.client.post(self.cexport_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 1)  # testing for error (invalid date syntax)
        post_data = {
            'sdate': "2020-01-01",
            'edate': "2100-01-01"
        }
        response = self.client.post(self.cexport_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['error'], 2)  # testing for error (end date has not yet happened)
        company.delete()
