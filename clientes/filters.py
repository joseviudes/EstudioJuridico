from django_filters import FilterSet, DateFromToRangeFilter
from .models import Cliente


class ClienteFilter(FilterSet):
    fecha_ingreso = DateFromToRangeFilter()

    class Meta:
        model = Cliente
        fields = ['fecha_ingreso']