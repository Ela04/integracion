from django.forms import ModelForm
from .models import Tb_Articulo

class ProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['patente','marca','modelo','categoria']

class ArticuloForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['patente','marca','modelo','categoria']