"""Camada de serviços do módulo de Clientes (Arquitetura 06)."""
import re

from django.utils import timezone

from .models import Customer

SESSION_KEY = "customer_data"


class CustomerService:
    """Gerencia os dados do cliente com persistência por sessão (Arquitetura 04)."""

    FIELDS = ["name", "phone", "address", "complement", "neighborhood", "city", "zip_code"]

    @staticmethod
    def normalize_phone(phone):
        return re.sub(r"\D", "", phone or "")

    @classmethod
    def get_or_create_customer(cls, data):
        """Cria ou atualiza o cliente usando o telefone como chave natural."""
        phone = cls.normalize_phone(data.get("phone"))
        defaults = {
            "name": data.get("name", "").strip(),
            "address": data.get("address", "").strip(),
            "complement": data.get("complement", "").strip(),
            "neighborhood": data.get("neighborhood", "").strip(),
            "city": data.get("city", "").strip(),
            "zip_code": data.get("zip_code", "").strip(),
        }
        customer, created = Customer.objects.get_or_create(phone=phone, defaults=defaults)
        if not created:
            # Atualiza com os dados mais recentes informados
            for field, value in defaults.items():
                if value:
                    setattr(customer, field, value)
            customer.save()
        return customer

    @classmethod
    def register_order_dates(cls, customer):
        now = timezone.now()
        if not customer.first_order_date:
            customer.first_order_date = now
        customer.last_order_date = now
        customer.save(update_fields=["first_order_date", "last_order_date", "updated_at"])

    # ---- Persistência dos dados no dispositivo (sessão) ----
    @classmethod
    def save_to_session(cls, request, data):
        request.session[SESSION_KEY] = {f: (data.get(f, "") or "").strip() for f in cls.FIELDS}
        request.session.modified = True

    @classmethod
    def load_from_session(cls, request):
        return request.session.get(SESSION_KEY, {})
