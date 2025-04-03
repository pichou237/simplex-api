from django.contrib import admin
from .models import User, OneTimePasscode,Technician

class AdminUser(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'address', 'city', 'phone_number')

admin.site.register(User, AdminUser)
admin.site.register(OneTimePasscode)

class TechnicienAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_verified', 'specialite', 'experience')
    list_filter = ('is_verified',)
    actions = ['valider_techniciens']

    @admin.action(description="Valider les techniciens sélectionnés")
    def valider_techniciens(self, request, queryset):
        queryset.update(is_verified=True)

admin.site.register(Technician, TechnicienAdmin)
