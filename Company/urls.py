# urls.py
from django.urls import path
from . import views


app_name = 'companies'

urlpatterns = [
    path('', views.company_home, name="company_home"),
    path('Show', views.company_list, name="companies_list"),
    path('New', views.new_company, name="new_company"),
    path('<slug:slug>', views.view_company, name="view_company"),
    path('<slug:slug>/Delete', views.delete_company, name="delete_company"),
    path('<slug:slug>/Update', views.update_company, name="update_company"),
    path('<slug:slug>/Export', views.export_company, name="single_export"),
]
