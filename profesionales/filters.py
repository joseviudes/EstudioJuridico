from django_filters import FilterSet, DateFromToRangeFilter
from .models import Profesional


class ProfesionalFilter(FilterSet):
    fecha_ingreso = DateFromToRangeFilter()

    class Meta:
        model = Profesional
        fields = ['fecha_ingreso']