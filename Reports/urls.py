from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
    path('',views.home,name="home"),
    path('data/',views.TableData,name="get-data"),
    path('summarizer/',views.SummarizeData,name="summarizer"),
    path('jointables/',views.JoinTables,name="jointables"),
    path('selectedtables/',views.SelectedTables,name="selectedtables"),
    path('joinresult/',views.JoinResult,name="joinresult"),
    path('filters/',views.FiltersPage,name="filters"),
    path('filtersDataByDate/',views.FiltersDataByDate,name="filtersdatabydate"),
    path('visualize/',views.VisualizeData,name="visualize"),
    
]
 


      