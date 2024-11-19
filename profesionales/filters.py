from django_filters import FilterSet, DateFromToRangeFilter
from .models import Profesional, Secretaria


class ProfesionalFilter(FilterSet):
    fecha_ingreso = DateFromToRangeFilter()

    class Meta:
        model = Profesional
        fields = ['fecha_ingreso']
        
        
class SecretariaFilter(FilterSet):
    fecha_ingreso = DateFromToRangeFilter()

    class Meta:
        model = Secretaria
        fields = ['fecha_ingreso']