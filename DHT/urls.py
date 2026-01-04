from django.urls import path
from . import views
from . import api
from .views import dashboard


urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", dashboard, name="dashboard"),
    path("api/", api.Dlist, name="json"),
    path("api/post/", api.Dhtviews.as_view(), name="dht_post"),
    path("download_csv/", views.download_csv, name="download_csv"),
    path("index/", views.table),
    path("myChart/", views.graphique),
    path("chart-data/", views.chart_data, name="chart_data"),
    path("chart-data-semaine/", views.chart_data_semaine, name="chart_data_semaine"),
    path("chart-data-jour/", views.chart_data_jour, name="chart_data_jour"),
    path("chart-data-mois/", views.chart_data_mois, name="chart_data_mois"),
    path('api/post/', views.post_dht, name='post_dht'),
    path('latest/', views.latest_json, name='latest_json'),
    path("api/incident/", api.incident_status, name="incident_status"),
    path('push-data/', api.push_data, name='push_data'),
    

    # ADMIN VIEW SITE
    path('', views.admin_dashboard, name='admin_dashboard'),
      path('chart/temperature/', views.chart_temperature, name='chart_temperature'),
    path('chart/humidity/', views.chart_humidity, name='chart_humidity'),
    # INCIDENTS
  path('incident/', views.incident_list, name='incident_list'),
  path('incident/<int:incident_id>/', views.incident_detail, name='incident_detail'),


   path('api/incident/<int:pk>/update/', views.update_incident, name='update_incident'),
    
  
     #path("login/", views.login_view, name="login"),
  


]

