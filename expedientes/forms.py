from django.forms import ModelForm, modelformset_factory
from django import forms
from .models import Expediente, Movimientos, Documentos

class ExpedienteForm(ModelForm):
    class Meta:
        model = Expediente
        fields = '__all__'
        exclude = ('tipo_expediente','estado')
        widgets = {
            'cliente': forms.Select(attrs={'class':'form-control', 'autofocus': 'autofocus'}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'fecha_finalizacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
            'caratula' : forms.TextInput(attrs={'class': 'form-control'})
        }
        
    def __init__(self, *args, **kwargs):
        super(ExpedienteForm, self).__init__(*args, **kwargs)
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
                

class MovimientosForm(ModelForm):
    class Meta:
        model = Movimientos
        fields = '__all__'
        exclude = ['expediente']
        widgets = {
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}, format='%Y-%m-%d'),
        }


    def __init__(self, *args, **kwargs):
        super(MovimientosForm, self).__init__(*args, **kwargs)
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
            # 'documentos': forms.ClearableFileInput(attrs={'multiple': True}), 
        }

DocumentoFormSet = modelformset_factory(Documentos, form=DocumentosForm, extra=1, can_delete=True)
