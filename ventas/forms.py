from django import forms
from projectcapriccio.ventas.models import Personalizado_item


class Personalizado_itemForm(forms.ModelForm):
    fecha_entrega = forms.DateField()
    
    class Meta:
        model = Personalizado_item
        fields = ('producto', 'mensaje', 'total', 'fecha_entrega')
