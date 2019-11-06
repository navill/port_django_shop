from django import forms

PRODUCT_QUANTITY = [(i, str(i)) for i in range(1, 100)]


class CartForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY, coerce=int)
    # cart_detail 페이지에서 update 동작 유무 판단
    is_update = forms.BooleanField(initial=False, required=False, widget=forms.HiddenInput)
