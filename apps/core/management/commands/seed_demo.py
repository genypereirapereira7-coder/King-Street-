"""Popula o banco com dados de demonstração para testes iniciais."""
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.coupons.models import Coupon
from apps.products.models import Category, Product, ProductVariation


class Command(BaseCommand):
    help = "Cria dados de demonstração (categorias, produtos, variações, cupom)."

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser("admin", "", "admin123")
            self.stdout.write(self.style.SUCCESS("Admin criado: admin / admin123"))

        data = {
            "Camisetas": [
                ("Camiseta King Oversized", "Algodão premium, corte oversized.", "199.90",
                 [("Preta", "P", 8), ("Preta", "M", 10), ("Preta", "G", 5), ("Branca", "M", 6)]),
                ("Camiseta Street Logo", "Estampa exclusiva King Street.", "149.90",
                 [("Preta", "M", 12), ("Preta", "G", 7), ("Cinza", "M", 4)]),
            ],
            "Moletons": [
                ("Moletom Royal Hoodie", "Moletom flanelado com capuz.", "329.90",
                 [("Preto", "M", 5), ("Preto", "G", 3), ("Bege", "G", 2)]),
            ],
            "Bonés": [
                ("Boné Crown Snapback", "Aba reta, ajuste snapback.", "119.90",
                 [("Preto", "Único", 15), ("Dourado", "Único", 6)]),
            ],
        }

        for cat_name, products in data.items():
            category, _ = Category.objects.get_or_create(name=cat_name)
            for name, desc, price, variations in products:
                product, created = Product.objects.get_or_create(
                    name=name,
                    defaults={
                        "description": desc,
                        "price": Decimal(price), "category": category,
                    },
                )
                if created:
                    for color, size, _qty in variations:
                        ProductVariation.objects.create(
                            product=product, color=color, size=size
                        )
                    self.stdout.write(f"Produto criado: {name}")

        today = timezone.localdate()
        Coupon.objects.get_or_create(
            code="KING10",
            defaults={
                "type": Coupon.TYPE_PERCENT, "value": Decimal("10"),
                "start_date": today, "end_date": today + timedelta(days=90),
                "is_active": True,
            },
        )
        self.stdout.write(self.style.SUCCESS("Dados de demonstração prontos!"))
