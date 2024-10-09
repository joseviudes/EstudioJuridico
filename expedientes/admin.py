from django.contrib import admin
from .models import Expediente, Movimientos
# Register your models here.

class ExpedienteAdmin(admin.ModelAdmin):
    list_display = ('numero_expediente', 'cliente', 'profesional', 'apoderado', 'fecha_inicio')


admin.site.register(Expediente, ExpedienteAdmin)
admin.site.register(Movimientos)

