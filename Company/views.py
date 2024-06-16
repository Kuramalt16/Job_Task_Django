import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Companies
import yfinance as yf
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import datetime


def company_home(request):
    return render(request, 'company/company_home.html')


def company_list(request):
    companies = Companies.objects.all().order_by('company_symbol')
    paginator = Paginator(companies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total_companies = paginator.count
    return render(request, 'company/company_list.html', {'page_obj': page_obj, 'company_count': total_companies})


def new_company(request):
    if request.method == "POST":
        ticker = request.POST.get('ticker')
        if Companies.objects.filter(company_symbol=ticker).exists():
            return render(request, 'company/new_company.html', {'error': 1, 'ticker': ticker})
        else:
            try:
                stock = yf.Ticker(ticker)
                company_name = stock.info["longName"]
            except KeyError:
                return render(request, 'company/new_company.html', {'error': 2, 'ticker': ticker})

            company_industry = stock.info["industry"]
            company_volume = stock.info["volume"]
            company_open = stock.info["open"]
            company_close = stock.info["previousClose"]
            company_high = stock.info["dayHigh"]

            company_low = stock.info["dayLow"]

            Companies.objects.create(
                company_symbol=ticker,
                company_name=company_name,
                company_industry=company_industry,
                company_volume=company_volume,
                company_open=company_open,
                company_close=company_close,
                company_high=company_high,
                company_low=company_low
            )

            return redirect('companies:companies_list')

    else:
        return render(request, 'company/new_company.html', {'error': 0})


def view_company(request, slug):
    if request.method == "POST":
        company = Companies.objects.get(company_symbol=slug)
        company.company_name = request.POST.get('name')
        company.company_industry = request.POST.get('industry')
        company.company_volume = request.POST.get('volume')
        company.company_open = request.POST.get('open')
        company.company_close = request.POST.get('close')
        company.company_high = request.POST.get('high')
        company.company_low = request.POST.get('low')
        company.date = timezone.now()
        company.save()

    company = Companies.objects.get(company_symbol=slug)
    return render(request, 'company/view_company.html', {'company': company})


def delete_company(request, slug):
    if request.method == "POST":
        company_symbol = request.POST.get('company_symbol')
        company = get_object_or_404(Companies, company_symbol=company_symbol)
        company.delete()
        return redirect('companies:companies_list')


def update_company(request, slug):
    if request.method == "POST":
        company = Companies.objects.get(company_symbol=slug)
        return render(request, 'company/update_company.html', {'company': company})


def export_company(request, slug):
    if request.method == "POST":
        start_date_str = request.POST.get('sdate')
        end_date_str = request.POST.get('edate')
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return render(request, 'company/export_single.html', {"error": 1})
        if start_date > end_date:
            return render(request, 'company/export_single.html', {"error": 1})
        elif end_date > datetime.now():
            return render(request, 'company/export_single.html', {"error": 2})
        stock = yf.Ticker(slug)
        historic_data = stock.history(start=start_date, end=end_date)
        filename = str(slug) + ".csv"
        response = HttpResponse(
            content_type="text/csv",
            headers={"Content-Disposition": f'attachment; filename="{filename}"'},
        )

        company = Companies.objects.get(company_symbol=slug)
        writer = csv.writer(response)
        writer.writerow(["Symbol", "Name", "Industry"])
        writer.writerow([slug, company.company_name, company.company_industry])
        writer.writerow(["Date", "Open", "Close", "Low", "High", "Volume", "Dividends"])
        for index, row in historic_data.iterrows():
            formatted_date = index
            writer.writerow([formatted_date, row['Open'],
                             row['Close'], row['Low'],
                             row['High'], row['Volume'],
                             row['Dividends']])
        return response
    return render(request, 'company/export_single.html', {"error": 0})
