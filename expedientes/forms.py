from django.forms import ModelForm, modelformset_factory
from django import forms
from .models import Expediente, Movimientos, Documentos
from datetime import timedelta, date

class ExpedienteForm(ModelForm):
    numero_expediente_preview = forms.CharField(
        required=False,  # No es obligatorio
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), 
        label="Número de Expediente (previsualización)"
    )

    # Agregar placeholder al campo apoderado
    apoderado = forms.CharField(
        max_length=250, 
        required=False, 
        widget=forms.TextInput(attrs={
            'placeholder': 'Apellido y Nombre (opcional)',
        })
    )
    class Meta:
        model = Expediente
        fields = '__all__'
        exclude = ('estado', 'numero_expediente')  # Excluimos 'numero_expediente' porque se genera automáticamente
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control', 'autofocus': 'autofocus'}),
            'jurisdiccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Justicia Federal de Corrientes'}),
            'dependencia': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Juzgado Federal de Corrientes 2'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'fecha_finalizacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'caratula': forms.TextInput(attrs={'class': 'form-control'}),
            'asunto': forms.Textarea(attrs={'cols': 40, 'rows': 2, 'placeholder': 'Escribe aqui'}),
            'tipo_expediente': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Recibe el usuario al inicializar
        super(ExpedienteForm, self).__init__(*args, **kwargs)

        # Calcula el rango de fechas permitidas para 'fecha_inicio'
        today = date.today()
        start_date = today - timedelta(days=2)  # 2 días antes
        end_date = today + timedelta(days=2)  # 2 días después
        
        # Establece los valores de min y max para el campo 'fecha_inicio'
        self.fields['fecha_inicio'].widget.attrs.update({
            'min': start_date.strftime('%Y-%m-%d'),
            'max': end_date.strftime('%Y-%m-%d'),
        })

        # Establece el valor mínimo de 'fecha_finalizacion' después de la 'fecha_inicio'
        if 'fecha_inicio' in self.data:
            fecha_inicio = self.data.get('fecha_inicio')
            if fecha_inicio:
                self.fields['fecha_finalizacion'].widget.attrs.update({
                    'min': fecha_inicio,
                })

        # Oculta el campo "profesional" si el usuario es abogado
        if user and user.rol == 'Abogado':
            self.fields.pop('profesional')

        # Generar el número de expediente de vista previa basado en el tipo de expediente seleccionado
        if self.instance and self.instance.tipo_expediente:
            self.fields['numero_expediente_preview'].initial = self.instance.generar_numero_expediente()

        # Marca los campos obligatorios con asterisco azul
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs.update({'class': 'form-control'})
                self.fields[field].label_suffix = ' <span class="text-primary">*</span>'
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control'})

    def clean(self):
        cleaned_data = super(ExpedienteForm, self).clean()

        # Generamos el número de expediente solo cuando se elige un tipo de expediente
        tipo_expediente = cleaned_data.get('tipo_expediente')
        if tipo_expediente:
            # Crear una instancia de Expediente solo para generar el número
            expediente = Expediente(tipo_expediente=tipo_expediente)
            cleaned_data['numero_expediente_preview'] = expediente.generar_numero_expediente()

        return cleaned_data

    def save(self, commit=True):
        instance = super(ExpedienteForm, self).save(commit=False)

        # Asigna automáticamente el profesional si el usuario es abogado
        if hasattr(self, 'user') and self.user.rol == 'Abogado':
            instance.profesional = self.user.profesional  # Ajusta el campo 'profesional' si tiene otro nombre

        if commit:
            instance.save()
        return instance


class MovimientosForm(ModelForm):
    class Meta:
        model = Movimientos
        fields = '__all__'
        exclude = ['expediente']
        widgets = {
            'fecha': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'placeholder': 'YYYY-MM-DD',
                },
                format='%Y-%m-%d'
            ),
            'tipo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tipo de movimiento'}),
            'detalle': forms.Textarea(attrs={'cols': 50, 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Recibimos el usuario si se pasa en la vista.
        super(MovimientosForm, self).__init__(*args, **kwargs)

        # Configurar rango de fechas dinámicamente
        min_date = (date.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        self.fields['fecha'].widget.attrs['min'] = min_date
        
        # Calcula el rango de fechas permitidas para 'fecha_inicio'
        today = date.today()
        start_date = today - timedelta(days=2)  # 2 días antes
        end_date = today + timedelta(days=2)  # 2 días después
        
        # Establece los valores de min y max para el campo 'fecha_inicio'
        self.fields['fecha'].widget.attrs.update({
            'min': start_date.strftime('%Y-%m-%d'),
            'max': end_date.strftime('%Y-%m-%d'),
        })


        # Si el usuario tiene el rol de 'Abogado', eliminamos el campo 'profesional'.
        if user and user.rol == 'Abogado':
            self.fields.pop('profesional')

        # Aplicar clases CSS y asteriscos a los campos requeridos.
        for field in self.fields:
            if self.fields[field].required:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })
                self.fields[field].label_suffix = ' *'
            else:
                self.fields[field].widget.attrs.update({
                    'class': 'form-control'
                })

class DocumentosForm(forms.ModelForm):
    class Meta:
        model = Documentos
        fields = ['documentos']
        widgets = {
            # Puedes habilitar múltiples archivos si es necesario.
            # 'documentos': forms.ClearableFileInput(attrs={'multiple': True}),
        }

DocumentoFormSet = modelformset_factory(Documentos, form=DocumentosForm, extra=1, can_delete=True)