"""Views da loja pública (Arquitetura 02/06).

As views apenas orquestram: recebem a requisição, chamam os serviços e
retornam a resposta. Nenhuma regra de negócio vive aqui.
"""
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.cart.services import CartService
from apps.customers.models import Customer
from apps.customers.services import CustomerService
from apps.orders.models import Order
from apps.orders.services import OrderService, WhatsAppService
from apps.products.models import Product
from apps.products.services import CatalogService
from apps.reviews.services import ReviewService

from .forms import CheckoutForm, ReviewForm


# ---------------------------------------------------------------------------
# Catálogo (página de entrada da loja)
# ---------------------------------------------------------------------------
def catalog(request):
    ordering = request.GET.get("ordem")
    products = CatalogService.filter_catalog(
        category_slug=request.GET.get("categoria") or None,
        color=request.GET.get("cor") or None,
        size=request.GET.get("tamanho") or None,
        min_price=request.GET.get("min") or None,
        max_price=request.GET.get("max") or None,
        query=request.GET.get("q") or None,
        ordering=ordering,
    )
    paginator = Paginator(products, 12)
    page = paginator.get_page(request.GET.get("page"))

    querystring = request.GET.copy()
    querystring.pop("page", None)

    return render(request, "store/catalog.html", {
        "page_obj": page,
        "categories": CatalogService.active_categories(),
        "query": request.GET.get("q", ""),
        "current_category": request.GET.get("categoria", ""),
        "current_ordering": ordering or "",
        "querystring": querystring.urlencode(),
    })


def product_detail(request, slug):
    product = CatalogService.get_available_product(slug)
    if product is None:
        messages.info(request, "Produto indisponível.")
        return redirect("store:catalog")

    customer = _current_customer(request)
    reviews = ReviewService.visible_for_product(product)
    can_review = ReviewService.can_review(customer, product) if customer else False

    return render(request, "store/product_detail.html", {
        "product": product,
        "variations": product.variations.all(),
        "reviews": reviews,
        "can_review": can_review,
        "review_form": ReviewForm(),
    })


# ---------------------------------------------------------------------------
# Carrinho
# ---------------------------------------------------------------------------
def cart_view(request):
    cart = CartService(request)
    return render(request, "store/cart.html", {
        "items": cart.items(),
        "subtotal": cart.subtotal(),
        "discount": cart.discount(),
        "total": cart.total(),
        "coupon": cart.coupon(),
    })


@require_POST
def cart_add(request):
    cart = CartService(request)
    variation_id = request.POST.get("variation_id")
    quantity = int(request.POST.get("quantity", 1) or 1)
    try:
        cart.add(variation_id, quantity)
        messages.success(request, "Produto adicionado ao carrinho.")
    except ValueError as exc:
        messages.warning(request, str(exc))
    next_url = request.POST.get("next") or "store:cart"
    return redirect(next_url)


@require_POST
def cart_update(request):
    cart = CartService(request)
    cart.set_quantity(request.POST.get("variation_id"), request.POST.get("quantity", 0))
    return redirect("store:cart")


@require_POST
def cart_remove(request):
    cart = CartService(request)
    cart.remove(request.POST.get("variation_id"))
    messages.info(request, "Item removido.")
    return redirect("store:cart")


@require_POST
def cart_apply_coupon(request):
    cart = CartService(request)
    try:
        cart.apply_coupon(request.POST.get("code"))
        messages.success(request, "Cupom aplicado.")
    except ValueError as exc:
        messages.warning(request, str(exc))
    return redirect("store:cart")


@require_POST
def cart_remove_coupon(request):
    CartService(request).remove_coupon()
    messages.info(request, "Cupom removido.")
    return redirect("store:cart")


# ---------------------------------------------------------------------------
# Finalização do pedido
# ---------------------------------------------------------------------------
def checkout(request):
    cart = CartService(request)
    if cart.is_empty():
        messages.info(request, "Seu carrinho está vazio.")
        return redirect("store:catalog")

    saved = CustomerService.load_from_session(request)

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # Persiste os dados no dispositivo para futuras compras
            CustomerService.save_to_session(request, data)
            try:
                order = OrderService.create_from_cart(request, cart, data)
            except ValueError as exc:
                messages.error(request, str(exc))
                return redirect("store:cart")
            # Pedido criado ANTES do redirecionamento ao WhatsApp
            return redirect("store:order_success", number=order.number)
    else:
        form = CheckoutForm(initial=saved)

    return render(request, "store/checkout.html", {
        "form": form,
        "items": cart.items(),
        "subtotal": cart.subtotal(),
        "discount": cart.discount(),
        "total": cart.total(),
        "coupon": cart.coupon(),
    })


def order_success(request, number):
    order = get_object_or_404(Order, number=number)
    whatsapp_url = WhatsAppService.build_url(order)
    # O carrinho é esvaziado após gerar o pedido (Arquitetura 04)
    CartService(request).clear()
    return render(request, "store/order_success.html", {
        "order": order,
        "whatsapp_url": whatsapp_url,
    })


# ---------------------------------------------------------------------------
# Área do cliente (consulta de pedidos)
# ---------------------------------------------------------------------------
def my_orders(request):
    customer = _current_customer(request)
    orders = []
    if customer:
        orders = customer.orders.prefetch_related("items").all()
    return render(request, "store/my_orders.html", {
        "customer": customer,
        "orders": orders,
    })


def order_track(request, number):
    order = get_object_or_404(Order.objects.prefetch_related("items", "history"), number=number)
    customer = _current_customer(request)
    # Só exibe se o pedido pertence ao cliente do dispositivo
    if not customer or order.customer_id != customer.id:
        messages.warning(request, "Pedido não encontrado para este dispositivo.")
        return redirect("store:my_orders")
    return render(request, "store/order_track.html", {"order": order})


@require_POST
def review_create(request, slug):
    product = get_object_or_404(Product, slug=slug)
    customer = _current_customer(request)
    form = ReviewForm(request.POST)
    if not form.is_valid():
        messages.warning(request, "Preencha a nota corretamente.")
        return redirect("store:product_detail", slug=slug)
    try:
        ReviewService.create_review(
            customer=customer,
            product=product,
            rating=form.cleaned_data["rating"],
            comment=form.cleaned_data["comment"],
            images=request.FILES.getlist("images"),
        )
        messages.success(request, "Avaliação enviada. Obrigado!")
    except ValueError as exc:
        messages.warning(request, str(exc))
    return redirect("store:product_detail", slug=slug)


# ---------------------------------------------------------------------------
# Apoio
# ---------------------------------------------------------------------------
def _current_customer(request):
    """Identifica o cliente do dispositivo pelo telefone salvo na sessão."""
    data = CustomerService.load_from_session(request)
    phone = CustomerService.normalize_phone(data.get("phone"))
    if not phone:
        return None
    return Customer.objects.filter(phone=phone).first()
