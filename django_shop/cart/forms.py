from django import forms

PRODUCT_QUANTITY = [(i, str(i)) for i in range(1, 100)]


class CartForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY, coerce=int)
