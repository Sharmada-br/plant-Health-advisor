from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # APIs
    path('api/plants/', views.plant_list_api),
    path('api/bulk-add/', views.bulk_add_data),
    path('search-suggestions/', views.search_suggestions),
]