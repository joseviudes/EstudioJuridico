from django.contrib import admin
from .models import Cliente
# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
    list_display = ['dni', 'apellido','nombre', 'fecha_nacimiento', 'telefono']
    search_fields = ['dni', 'apellido','nombre']

admin.site.register(Cliente, ClienteAdmin)

