from django.contrib import admin
from .models import Profesional, Secretaria
# Register your models here.

class ProfesionalAdmin(admin.ModelAdmin):
    list_display = ('idMatriculaProf', 'apellido', 'nombre', 'dni', 'estado')

admin.site.register(Profesional, ProfesionalAdmin)

admin.site.register(Secretaria)