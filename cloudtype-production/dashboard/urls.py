from django.urls import path
from .views import dashboard_overview

urlpatterns = [
    path('<int:cafe_id>/', dashboard_overview, name='dashboard_overview'),
]