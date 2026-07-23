"""Serviços do painel — indicadores do dashboard (Arquitetura 05)."""
from django.conf import settings
from django.db.models import Count, F, Sum
from django.utils import timezone

from apps.customers.models import Customer
from apps.orders.models import Order, OrderItem, OrderStatus
from apps.products.models import Product, ProductVariation


class DashboardService:
    @staticmethod
    def summary():
        today = timezone.localdate()
        orders = Order.objects.all()
        low_stock = (
            ProductVariation.objects.filter(stock_quantity__lte=settings.LOW_STOCK_THRESHOLD)
            .select_related("product")
            .order_by("stock_quantity")
        )
        return {
            "total_orders": orders.count(),
            "orders_today": orders.filter(created_at__date=today).count(),
            "orders_preparing": orders.filter(status=OrderStatus.PREPARING).count(),
            "orders_delivered": orders.filter(status=OrderStatus.DELIVERED).count(),
            "total_products": Product.objects.count(),
            "total_customers": Customer.objects.count(),
            "low_stock": low_stock[:10],
            "low_stock_count": low_stock.count(),
            "recent_orders": orders.select_related("customer")[:8],
            "best_sellers": (
                OrderItem.objects.values("product_name")
                .annotate(qty=Sum("quantity"))
                .order_by("-qty")[:5]
            ),
        }
