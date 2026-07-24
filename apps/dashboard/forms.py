from django import forms

from apps.coupons.models import Coupon
from apps.products.models import Category, Product, ProductVariation


class BaseStyledForm(forms.ModelForm):
    """Aplica classe CSS padrão do painel a todos os campos."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            css = "field-input"
            if isinstance(widget, forms.CheckboxInput):
                css = "field-check"
            elif isinstance(widget, forms.Select):
                css = "field-input field-select"
            existing = widget.attrs.get("class", "")
            widget.attrs["class"] = f"{existing} {css}".strip()


class CategoryForm(BaseStyledForm):
    class Meta:
        model = Category
        fields = ["name", "description", "is_active"]


class ProductForm(BaseStyledForm):
    class Meta:
        model = Product
        fields = ["name", "description", "price", "category", "status"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}


class VariationForm(BaseStyledForm):
    class Meta:
        model = ProductVariation
        fields = ["color", "size"]


class CouponForm(BaseStyledForm):
    class Meta:
        model = Coupon
        fields = ["code", "type", "value", "start_date", "end_date", "is_active", "max_uses"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
