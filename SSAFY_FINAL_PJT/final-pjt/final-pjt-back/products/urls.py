from django.urls import path
from . import views


urlpatterns = [
    path('save_products_db/', views.deposit_and_saving_list),
    path('exchange_rates/', views.exchange_rate),

    path('data_load/bank/', views.bank),
    path('data_load/depositproduct/', views.depositproduct),
    path('data_load/deposit/', views.deposit),
    path('data_load/savingproduct/', views.savingproduct),
    path('data_load/saving/', views.saving),

]
