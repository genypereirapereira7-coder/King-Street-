from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "store"

urlpatterns = [
    # A entrada do site abre direto no catálogo
    path("", RedirectView.as_view(pattern_name="store:catalog", permanent=False), name="home"),
    path("catalogo/", views.catalog, name="catalog"),
    path("buscar/", views.catalog, name="search"),
    path("produto/<slug:slug>/", views.product_detail, name="product_detail"),
    path("produto/<slug:slug>/avaliar/", views.review_create, name="review_create"),

    # Carrinho
    path("carrinho/", views.cart_view, name="cart"),
    path("carrinho/adicionar/", views.cart_add, name="cart_add"),
    path("carrinho/atualizar/", views.cart_update, name="cart_update"),
    path("carrinho/remover/", views.cart_remove, name="cart_remove"),
    path("carrinho/cupom/aplicar/", views.cart_apply_coupon, name="cart_apply_coupon"),
    path("carrinho/cupom/remover/", views.cart_remove_coupon, name="cart_remove_coupon"),

    # Finalização
    path("finalizar/", views.checkout, name="checkout"),
    path("pedido/<str:number>/sucesso/", views.order_success, name="order_success"),

    # Área do cliente
    path("meus-pedidos/", views.my_orders, name="my_orders"),
    path("pedido/<str:number>/", views.order_track, name="order_track"),
]
