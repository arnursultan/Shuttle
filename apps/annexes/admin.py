from django.contrib import admin
from .models import (
    Category, Review, Certificate, Application, Building,
    Driver, DriverProfile, Car, Profile, Route
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
    ordering = ('title',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('text', 'image')
    search_fields = ('text',)
    ordering = ('-id',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('image',)
    ordering = ('-id',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('description', 'review', 'message')
    search_fields = ('description', 'review', 'message')
    ordering = ('-id',)

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('image', 'details')
    search_fields = ('details',)
    ordering = ('-id',)

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('wallet_balance', 'region')
    search_fields = ('region',)
    list_filter = ('region',)
    ordering = ('-id',)

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('wallet_balance', 'service_type', 'region')
    list_filter = ('service_type', 'region')
    search_fields = ('service_type', 'region')
    ordering = ('-id',)

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'color', 'license_plate')
    search_fields = ('make', 'model', 'license_plate')
    list_filter = ('make', 'model')
    ordering = ('make', 'model')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_type', 'experience', 'phone_number', 'rating', 'car')
    list_filter = ('user_type', 'rating')
    search_fields = ('name', 'phone_number')
    ordering = ('name',)

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('start_point', 'end_point', 'traffic_condition')
    list_filter = ('traffic_condition',)
    search_fields = ('start_point', 'end_point')
    ordering = ('-id',)
