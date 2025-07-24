from django import forms
from .models import Producto, Venta

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio']

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['producto', 'cantidad', 'fecha', 'total']


class FiltroVentasForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.all(), required=False)
    fecha_inicio = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    fecha_fin = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}), required=False)
    precio_minimo = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    precio_maximo = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    estado = forms.ChoiceField(
        choices=[('', '------')] + Venta.ESTADO_CHOICES,  # Agrega un valor vacío al inicio
        required=False,
    )
