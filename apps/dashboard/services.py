"""Serviços do painel — indicadores do dashboard (Arquitetura 05)."""
from django.db.models import Count, Q, Sum
from django.utils import timezone

from apps.customers.models import Customer
from apps.orders.models import Order, OrderItem, OrderStatus
from apps.products.models import Product


class DashboardService:
    @staticmethod
    def summary():
        today = timezone.localdate()

        # Um único SELECT para todos os contadores de pedidos, em vez de
        # quatro consultas separadas — o painel abre bem mais rápido.
        totals = Order.objects.aggregate(
            total=Count("id"),
            today=Count("id", filter=Q(created_at__date=today)),
            preparing=Count("id", filter=Q(status=OrderStatus.PREPARING)),
            delivered=Count("id", filter=Q(status=OrderStatus.DELIVERED)),
        )

        return {
            "total_orders": totals["total"],
            "orders_today": totals["today"],
            "orders_preparing": totals["preparing"],
            "orders_delivered": totals["delivered"],
            "total_products": Product.objects.count(),
            "total_customers": Customer.objects.count(),
            "recent_orders": Order.objects.select_related("customer")[:8],
            "best_sellers": (
                OrderItem.objects.values("product_name")
                .annotate(qty=Sum("quantity"))
                .order_by("-qty")[:5]
            ),
        }
