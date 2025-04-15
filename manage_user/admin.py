from django.contrib import admin
from .models import User, OneTimePasscode, Technician, MetaUser, Client

class AdminUser(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'address', 'city', 'phone_number')
    search_fields = ('email', 'first_name', 'last_name')

admin.site.register(User, AdminUser)
admin.site.register(OneTimePasscode)
admin.site.register(Client)
admin.site.register(MetaUser)

class TechnicienAdmin(admin.ModelAdmin):
    list_display = ( 'profession', 'is_verified')
    list_filter = ['is_verified']
    search_fields = ['profession']
    actions = ['valider_techniciens']

    @admin.action(description="Valider les techniciens sélectionnés")
    def valider_techniciens(self, request, queryset): 
        queryset.update(is_verified=True)

admin.site.register(Technician, TechnicienAdmin)
