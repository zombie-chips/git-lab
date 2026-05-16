from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'readings'

urlpatterns = [
    # Главная
    path('', views.home_view, name='home'),

    # Аутентификация
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='readings:login'), name='logout'),
    path('profile/', views.profile_view, name='profile'),

    # CRUD для TemperatureReading
    path('readings/', views.ReadingListView.as_view(), name='reading_list'),
    path('readings/<int:pk>/', views.ReadingDetailView.as_view(), name='reading_detail'),
    path('readings/create/', views.ReadingCreateView.as_view(), name='reading_create'),
    path('readings/<int:pk>/update/', views.ReadingUpdateView.as_view(), name='reading_update'),
    path('readings/<int:pk>/delete/', views.ReadingDeleteView.as_view(), name='reading_delete'),

    # CRUD для Location
    path('locations/', views.LocationListView.as_view(), name='location_list'),
    path('locations/create/', views.LocationCreateView.as_view(), name='location_create'),
    path('locations/<int:pk>/update/', views.LocationUpdateView.as_view(), name='location_update'),
    path('locations/<int:pk>/delete/', views.LocationDeleteView.as_view(), name='location_delete'),

    # CRUD для Sensor
    path('sensors/', views.SensorListView.as_view(), name='sensor_list'),
    path('sensors/create/', views.SensorCreateView.as_view(), name='sensor_create'),
    path('sensors/<int:pk>/update/', views.SensorUpdateView.as_view(), name='sensor_update'),
    path('sensors/<int:pk>/delete/', views.SensorDeleteView.as_view(), name='sensor_delete'),
]