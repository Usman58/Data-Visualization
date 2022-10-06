from django.contrib import admin
from django.urls import path
from .import views


urlpatterns = [
    path('',views.home,name="home"),
    path('data/',views.TableData,name="get-data"),
    #path('columns/',views.TableColumns,name="get-columns"),
    path('summarizer/',views.SummarizeData,name="summarizer"),
    path('jointables/',views.JoinTables,name="jointables"),
    path('selectedtables/',views.SelectedTables,name="selectedtables"),
    path('joinresult/',views.JoinResult,name="joinresult"),
    path('filters/',views.Filters,name="filters"),
    path('filtersData/',views.FiltersData,name="filtersdata"),
    
]
 


      