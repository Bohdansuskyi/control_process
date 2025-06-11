from django.urls import path
from . import views
from .views import StationCreateView,RecordsCreateView

urlpatterns = [
    path('', views.index, name='index'),
    path('info/', views.info, name='info'),
    path('charts/', views.charts, name='charts'),

    # rest framework
    path("station/",views.StationListCreate.as_view(),name="station-view-create"),
    path("records/",views.RecordsListCreate.as_view(),name="records-view-create"),
    
    # endpoints
    path("create-station/",StationCreateView.as_view(),name='station-create'),
    path("create-records/",RecordsCreateView.as_view(),name="records-create")
]
