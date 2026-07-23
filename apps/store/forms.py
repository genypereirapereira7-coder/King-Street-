from django import forms

from apps.orders.models import DeliveryMethod


class CheckoutForm(forms.Form):
    """Dados solicitados apenas na finalização do pedido (Arquitetura 04)."""

    name = forms.CharField(label="Nome completo", max_length=160)
    phone = forms.CharField(label="Telefone / WhatsApp", max_length=20)
    delivery_method = forms.ChoiceField(
        label="Forma de entrega", choices=DeliveryMethod.choices,
        widget=forms.RadioSelect, initial=DeliveryMethod.PICKUP,
    )
    address = forms.CharField(label="Endereço", max_length=200, required=False)
    complement = forms.CharField(label="Complemento", max_length=120, required=False)
    neighborhood = forms.CharField(label="Bairro", max_length=120, required=False)
    city = forms.CharField(label="Cidade", max_length=120, required=False)
    zip_code = forms.CharField(label="CEP", max_length=15, required=False)
    notes = forms.CharField(label="Observações", widget=forms.Textarea(attrs={"rows": 2}), required=False)

    def clean_phone(self):
        import re

        digits = re.sub(r"\D", "", self.cleaned_data["phone"])
        if len(digits) < 10:
            raise forms.ValidationError("Informe um telefone válido com DDD.")
        return self.cleaned_data["phone"]

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("delivery_method") == DeliveryMethod.DELIVERY:
            required = {"address": "Endereço", "neighborhood": "Bairro", "city": "Cidade"}
            for field, label in required.items():
                if not cleaned.get(field):
                    self.add_error(field, f"{label} é obrigatório para entrega.")
        return cleaned


class ReviewForm(forms.Form):
    rating = forms.IntegerField(label="Nota", min_value=1, max_value=5)
    comment = forms.CharField(label="Comentário", widget=forms.Textarea(attrs={"rows": 3}), required=False)
