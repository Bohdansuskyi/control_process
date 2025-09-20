from django.urls import path
from django.contrib import admin
from . import views
from .views import RecordsCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('info/', views.info, name='info'),
    path('charts/', views.charts, name='charts'),

    # rest framework
    path("records/",views.RecordsListCreate.as_view(),name="records-view-create"),
    
    # endpoints
    path("create-records/",RecordsCreateView.as_view(),name="records-create"),
    path('api/check_update/', views.check_data_update, name='check_data_update'),

]
