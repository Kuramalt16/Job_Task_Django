from django.db import models
import yfinance as yf
class Companies(models.Model):
    company_name = models.CharField(max_length=200)
    company_symbol = models.CharField(max_length=10)
    company_industry = models.CharField(max_length=100)
    company_volume = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_symbol

# class Get_data_form_yf(models.Model):
#     ticker = models.
