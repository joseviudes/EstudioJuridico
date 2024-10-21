from django_filters import FilterSet, DateFromToRangeFilter
from .models import Expediente


class ExpedienteFilter(FilterSet):
    fecha_ingreso = DateFromToRangeFilter()

    class Meta:
        model = Expediente
        fields = ['fecha_inicio']