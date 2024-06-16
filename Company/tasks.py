from celery import shared_task
import yfinance as yf
from .models import Companies
from datetime import datetime

@shared_task
def update_company_data():
    companies = Companies.objects.all()
    for company in companies:
        ticker = yf.Ticker(company.company_symbol)
        info = ticker.info

        company.company_name = info.get('longName', company.company_name)
        company.company_industry = info.get('industry', company.company_industry)
        company.company_volume = info.get('volume', company.company_volume)
        company.company_open = info.get('open', company.company_open)
        company.company_close = info.get('previousClose', company.company_close)
        company.company_high = info.get('dayHigh', company.company_high)
        company.company_low = info.get('dayLow', company.company_low)
        company.date = datetime.now()

        company.save()

    print("Task Completed!")
