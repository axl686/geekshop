from authapp.forms import ShopUserEditForm
from authapp.models import ShopUser
from django import forms
from mainapp.models import ProductCategory, Product


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductCategoryEditForm(forms.ModelForm):
    discount = forms.IntegerField(label='Скидка', required=False, min_value=0, max_value=90, initial=0)

    class Meta:
        model = ProductCategory
        fields = '__all__'

    def __init__(self, *arg, **kwargs):
        super(ProductCategoryEditForm, self).__init__(*arg, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *arg, **kwargs):
        super(ProductEditForm, self).__init__(*arg, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''


class ProductReadForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'name', 'short_desc', 'description', 'price', 'quantity', 'is_active')

    def __init__(self, *arg, **kwargs):
        super(ProductReadForm, self).__init__(*arg, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
