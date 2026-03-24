from django.contrib import admin
from .models import Appointment, Therapy


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = ('patient', 'therapy', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'therapy')
    search_fields = ('patient__name', 'therapy__therapy_name')
    ordering = ('-date', '-time')

    fieldsets = (
        ("Patient Info", {
            'fields': ('patient',)
        }),
        ("Therapy Info", {
            'fields': ('therapy',)
        }),
        ("Schedule", {
            'fields': ('date', 'time')
        }),
        ("Status", {
            'fields': ('status',)
        }),
    )

    list_editable = ('status',)


@admin.register(Therapy)
class TherapyAdmin(admin.ModelAdmin):
    list_display = ('therapy_name', 'duration')
    search_fields = ('therapy_name',)