from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import TemperatureReading, Sensor, Location
from .forms import TemperatureReadingForm, RegistrationForm
from .mixins import MeteorologistRequiredMixin, AdminRequiredMixin, CanEditReadingMixin
from django.contrib.auth.models import User


# CRUD для TemperatureReading с разграничением прав
class ReadingListView(LoginRequiredMixin, ListView):
    model = TemperatureReading
    template_name = 'readings/reading_list.html'
    context_object_name = 'readings'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'profile') and user.profile.role == 'admin':
            return TemperatureReading.objects.all()
        elif hasattr(user, 'profile') and user.profile.role == 'meteorologist':
            return TemperatureReading.objects.all()
        else:
            return TemperatureReading.objects.filter(created_by=user)


class ReadingDetailView(LoginRequiredMixin, DetailView):
    model = TemperatureReading
    template_name = 'readings/reading_detail.html'
    context_object_name = 'reading'


class ReadingCreateView(LoginRequiredMixin, MeteorologistRequiredMixin, CreateView):
    model = TemperatureReading
    form_class = TemperatureReadingForm
    template_name = 'readings/reading_form.html'
    success_url = reverse_lazy('reading_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ReadingUpdateView(LoginRequiredMixin, CanEditReadingMixin, UpdateView):
    model = TemperatureReading
    form_class = TemperatureReadingForm
    template_name = 'readings/reading_form.html'
    success_url = reverse_lazy('reading_list')


class ReadingDeleteView(LoginRequiredMixin, CanEditReadingMixin, DeleteView):
    model = TemperatureReading
    template_name = 'readings/reading_confirm_delete.html'
    success_url = reverse_lazy('reading_list')


# Представления для управления всеми сущностями
class LocationListView(LoginRequiredMixin, MeteorologistRequiredMixin, ListView):
    model = Location
    template_name = 'readings/location_list.html'
    context_object_name = 'locations'


class LocationCreateView(LoginRequiredMixin, MeteorologistRequiredMixin, CreateView):
    model = Location
    fields = ['name', 'latitude', 'longitude', 'country', 'climate_zones', 'elevation']
    template_name = 'readings/location_form.html'
    success_url = reverse_lazy('location_list')


class LocationUpdateView(LoginRequiredMixin, MeteorologistRequiredMixin, UpdateView):
    model = Location
    fields = ['name', 'latitude', 'longitude', 'country', 'climate_zones', 'elevation']
    template_name = 'readings/location_form.html'
    success_url = reverse_lazy('location_list')


class LocationDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Location
    template_name = 'readings/location_confirm_delete.html'
    success_url = reverse_lazy('location_list')


class SensorListView(LoginRequiredMixin, MeteorologistRequiredMixin, ListView):
    model = Sensor
    template_name = 'readings/sensor_list.html'
    context_object_name = 'sensors'


class SensorCreateView(LoginRequiredMixin, MeteorologistRequiredMixin, CreateView):
    model = Sensor
    fields = ['serial_number', 'location', 'installation_date', 'is_active']
    template_name = 'readings/sensor_form.html'
    success_url = reverse_lazy('sensor_list')


class SensorUpdateView(LoginRequiredMixin, MeteorologistRequiredMixin, UpdateView):
    model = Sensor
    fields = ['serial_number', 'location', 'installation_date', 'is_active']
    template_name = 'readings/sensor_form.html'
    success_url = reverse_lazy('sensor_list')


class SensorDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    model = Sensor
    template_name = 'readings/sensor_confirm_delete.html'
    success_url = reverse_lazy('sensor_list')


# Регистрация и аутентификация
class RegisterView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'readings/register.html'
    success_url = reverse_lazy('login')


class CustomLoginView(LoginView):
    template_name = 'readings/login.html'
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = 'readings:login'


@login_required
def profile_view(request):
    return render(request, 'readings/profile.html')


@login_required
def home_view(request):
    return render(request, 'readings/home.html')