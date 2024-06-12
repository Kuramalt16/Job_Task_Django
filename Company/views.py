
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Companies
import yfinance as yf
from django.core.paginator import Paginator
from datetime import datetime

def Company_home(request):
    return render(request, 'company/company_home.html')

def Company_list(request):
    companies = Companies.objects.all().order_by('company_symbol')
    paginator = Paginator(companies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    total_companies = paginator.count
    return render(request, 'company/company_list.html', {'page_obj': page_obj, 'company_count': total_companies})

def New_Company(request):
    if request.method == "POST":
        ticker = request.POST.get('ticker')
        if Companies.objects.filter(company_symbol=ticker).exists():
            return render(request, 'company/new_company.html', {'error': 1, 'ticker': ticker})
        else:
            try:
                stock = yf.Ticker(ticker)
                company_name = stock.info["longName"]
                company_industry = stock.info["industry"]
                company_volume = stock.info["volume"]

                company = Companies.objects.update_or_create(
                    company_symbol=ticker,
                    defaults={
                        'company_name': company_name,
                        'company_industry': company_industry,
                        'company_volume': company_volume
                    }
                )
                return redirect('companies:campanies_list')
            except KeyError:
                return render(request, 'company/new_company.html', {'error': 2, 'ticker': ticker})
    else:
        return render(request, 'company/new_company.html', {'error': 0})

def View_Company(request, slug):
    if request.method == "POST":
        company = Companies.objects.get(company_symbol=slug)
        company.company_name = request.POST.get('name')
        company.company_industry = request.POST.get('industry')
        company.company_volume = request.POST.get('volume')
        company.date = datetime.now()
        company.save()

    company = Companies.objects.get(company_symbol=slug)
    return render(request, 'company/view_company.html', {'company': company})

def Delete_Company(request, slug):
    company = Companies.objects.get(company_symbol=slug)
    company.delete()
    return redirect('companies:campanies_list')

def Update_Company(request, slug):
    company = Companies.objects.get(company_symbol=slug)
    return render(request, 'company/update_company.html', {'company': company})

def Export_companies(request):
    companies = Companies.objects.all()
    return render(request, 'company/export.html', {'companies': companies})
