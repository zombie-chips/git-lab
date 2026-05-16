from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Country, ClimateZone, Location, Sensor, TemperatureReading, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = [UserProfileInline]
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_role']

    def get_role(self, obj):
        return obj.profile.get_role_display()

    get_role.short_description = 'Роль'


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name']


class ClimateZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'country']
    list_filter = ['country', 'climate_zones']
    search_fields = ['name', 'country__name']
    filter_horizontal = ['climate_zones']


class SensorAdmin(admin.ModelAdmin):
    list_display = ['serial_number', 'location', 'installation_date', 'is_active']
    list_filter = ['is_active', 'installation_date']
    search_fields = ['serial_number', 'location__name']


class TemperatureReadingAdmin(admin.ModelAdmin):
    list_display = ['id', 'sensor', 'temperature', 'timestamp', 'created_by']
    list_filter = ['sensor__location__country', 'timestamp', 'created_by']
    search_fields = ['sensor__serial_number', 'sensor__location__name']
    raw_id_fields = ['created_by']


admin.site.register(Country, CountryAdmin)
admin.site.register(ClimateZone, ClimateZoneAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(TemperatureReading, TemperatureReadingAdmin)