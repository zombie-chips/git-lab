from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название страны")
    code = models.CharField(max_length=3, unique=True, verbose_name="Код страны")

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class ClimateZone(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название зоны")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Климатическая зона"
        verbose_name_plural = "Климатические зоны"

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название локации")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Широта")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name="Долгота")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='locations', verbose_name="Страна")
    climate_zones = models.ManyToManyField(ClimateZone, related_name='locations', blank=True,
                                           verbose_name="Климатические зоны")
    elevation = models.IntegerField(null=True, blank=True, verbose_name="Высота над уровнем моря (м)")

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"
        unique_together = ['latitude', 'longitude']

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"


class Sensor(models.Model):
    serial_number = models.CharField(max_length=50, unique=True, verbose_name="Серийный номер")
    location = models.OneToOneField(Location, on_delete=models.CASCADE, related_name='sensor', verbose_name="Локация")
    installation_date = models.DateField(verbose_name="Дата установки")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Датчик"
        verbose_name_plural = "Датчики"

    def __str__(self):
        return f"Сенсор {self.serial_number} - {self.location.name}"


class TemperatureReading(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='readings', verbose_name="Датчик")
    temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Температура (°C)")
    timestamp = models.DateTimeField(default=timezone.now, verbose_name="Дата и время")
    note = models.TextField(blank=True, verbose_name="Примечание")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Кем добавлено")

    class Meta:
        verbose_name = "Температурное показание"
        verbose_name_plural = "Температурные показания"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M')} - {self.sensor.location.name}: {self.temperature}°C"

    def get_absolute_url(self):
        return reverse('reading_detail', args=[str(self.id)])


# Расширение профиля пользователя
class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('observer', 'Наблюдатель'),
        ('meteorologist', 'Метеоролог'),
        ('admin', 'Администратор'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='observer', verbose_name="Роль")
    organization = models.CharField(max_length=200, blank=True, verbose_name="Организация")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"