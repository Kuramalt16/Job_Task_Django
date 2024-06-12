# urls.py
from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('', views.Company_home),
    path('Show', views.Company_list, name="campanies_list"),
    path('New', views.New_Company, name="new_company"),
    path('Export', views.Export_companies),
    path('<slug:slug>', views.View_Company, name="view_company"),
    path('<slug:slug>/Delete', views.Delete_Company),
    path('<slug:slug>/Update', views.Update_Company),
]
