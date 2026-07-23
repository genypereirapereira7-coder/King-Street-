from django.urls import path

from . import views

app_name = "dashboard"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("sair/", views.logout_view, name="logout"),
    path("", views.home, name="home"),

    # Produtos
    path("produtos/", views.product_list, name="product_list"),
    path("produtos/novo/", views.product_create, name="product_create"),
    path("produtos/<int:pk>/", views.product_edit, name="product_edit"),
    path("produtos/<int:pk>/excluir/", views.product_delete, name="product_delete"),
    path("produtos/<int:pk>/status/", views.product_toggle_status, name="product_toggle_status"),
    path("produtos/<int:pk>/variacao/", views.variation_add, name="variation_add"),
    path("variacao/<int:pk>/estoque/", views.variation_update_stock, name="variation_update_stock"),
    path("variacao/<int:pk>/excluir/", views.variation_delete, name="variation_delete"),
    path("produtos/<int:pk>/imagem/", views.image_add, name="image_add"),
    path("imagem/<int:pk>/excluir/", views.image_delete, name="image_delete"),

    # Categorias
    path("categorias/", views.category_list, name="category_list"),
    path("categorias/<int:pk>/", views.category_edit, name="category_edit"),
    path("categorias/<int:pk>/ativar/", views.category_toggle, name="category_toggle"),
    path("categorias/<int:pk>/excluir/", views.category_delete, name="category_delete"),

    # Pedidos
    path("pedidos/", views.order_list, name="order_list"),
    path("pedidos/<str:number>/", views.order_detail, name="order_detail"),
    path("pedidos/<str:number>/status/", views.order_change_status, name="order_change_status"),

    # Clientes
    path("clientes/", views.customer_list, name="customer_list"),
    path("clientes/<int:pk>/", views.customer_detail, name="customer_detail"),

    # Cupons
    path("cupons/", views.coupon_list, name="coupon_list"),
    path("cupons/<int:pk>/", views.coupon_edit, name="coupon_edit"),
    path("cupons/<int:pk>/status/", views.coupon_toggle, name="coupon_toggle"),

    # Avaliações
    path("avaliacoes/", views.review_list, name="review_list"),
    path("avaliacoes/<int:pk>/ocultar/", views.review_toggle, name="review_toggle"),
    path("avaliacoes/<int:pk>/excluir/", views.review_delete, name="review_delete"),
]
