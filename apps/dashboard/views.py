"""Views do painel administrativo (Arquitetura 05).

Painel exclusivo do proprietário, separado da loja pública. As views apenas
orquestram; as regras ficam nas camadas de serviço dos módulos.
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.coupons.models import Coupon
from apps.customers.models import Customer
from apps.orders.models import Order, OrderStatus
from apps.orders.services import OrderService, WhatsAppService
from apps.products.models import Category, Product, ProductImage, ProductVariation
from apps.products.services import ProductImageService
from apps.reviews.models import Review

from .forms import CategoryForm, CouponForm, ProductForm, VariationForm
from .services import DashboardService

staff_required = user_passes_test(lambda u: u.is_active and u.is_staff, login_url="dashboard:login")


# ---------------------------------------------------------------------------
# Autenticação
# ---------------------------------------------------------------------------
def login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("dashboard:home")
    if request.method == "POST":
        user = authenticate(
            request, username=request.POST.get("username"), password=request.POST.get("password")
        )
        if user and user.is_staff:
            login(request, user)
            return redirect("dashboard:home")
        messages.error(request, "Usuário ou senha inválidos.")
    return render(request, "dashboard/login.html")


def logout_view(request):
    logout(request)
    return redirect("dashboard:login")


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------
@login_required
@staff_required
def home(request):
    return render(request, "dashboard/home.html", {"data": DashboardService.summary()})


# ---------------------------------------------------------------------------
# Produtos
# ---------------------------------------------------------------------------
@login_required
@staff_required
def product_list(request):
    query = request.GET.get("q", "").strip()
    products = Product.objects.select_related("category").prefetch_related("images")
    if query:
        products = products.filter(Q(name__icontains=query))
    page = Paginator(products, 20).get_page(request.GET.get("page"))
    return render(request, "dashboard/product_list.html", {"page_obj": page, "query": query})


@login_required
@staff_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, "Produto criado. Agora adicione variações e imagens.")
            return redirect("dashboard:product_edit", pk=product.pk)
    else:
        form = ProductForm()
    return render(request, "dashboard/product_form.html", {"form": form, "creating": True})


@login_required
@staff_required
def product_edit(request, pk):
    product = get_object_or_404(
        Product.objects.prefetch_related("variations", "images"), pk=pk
    )
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado.")
            return redirect("dashboard:product_edit", pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, "dashboard/product_form.html", {
        "form": form,
        "product": product,
        "variation_form": VariationForm(),
        "remaining_images": ProductImageService.remaining_slots(product),
    })


@login_required
@staff_required
@require_POST
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.info(request, "Produto excluído.")
    return redirect("dashboard:product_list")


@login_required
@staff_required
@require_POST
def product_toggle_status(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.status = (
        Product.STATUS_INACTIVE if product.status == Product.STATUS_ACTIVE else Product.STATUS_ACTIVE
    )
    product.save(update_fields=["status", "updated_at"])
    messages.success(request, "Status atualizado.")
    return redirect(request.POST.get("next") or "dashboard:product_list")


# ---- Variações ----
@login_required
@staff_required
@require_POST
def variation_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = VariationForm(request.POST)
    if form.is_valid():
        variation = form.save(commit=False)
        variation.product = product
        try:
            variation.save()
            messages.success(request, "Variação adicionada.")
        except Exception:
            messages.warning(request, "Essa combinação de cor e tamanho já existe.")
    else:
        messages.warning(request, "Dados da variação inválidos.")
    return redirect("dashboard:product_edit", pk=pk)


@login_required
@staff_required
@require_POST
def variation_delete(request, pk):
    variation = get_object_or_404(ProductVariation, pk=pk)
    product_id = variation.product_id
    variation.delete()
    messages.info(request, "Variação removida.")
    return redirect("dashboard:product_edit", pk=product_id)


# ---- Imagens ----
@login_required
@staff_required
@require_POST
def image_add(request, pk):
    """Recebe uma ou várias fotos de uma vez (até completar o limite de 3)."""
    product = get_object_or_404(Product, pk=pk)
    images = request.FILES.getlist("images") or request.FILES.getlist("image")
    if not images:
        messages.warning(request, "Selecione pelo menos uma foto.")
        return redirect("dashboard:product_edit", pk=pk)
    try:
        adicionadas, ignoradas = ProductImageService.add_images(product, images)
        plural = "s" if adicionadas > 1 else ""
        messages.success(request, f"{adicionadas} foto{plural} adicionada{plural}.")
        if ignoradas:
            messages.warning(
                request, f"{ignoradas} foto(s) não couberam: o limite é de 3 por produto."
            )
    except ValueError as exc:
        messages.warning(request, str(exc))
    return redirect("dashboard:product_edit", pk=pk)


@login_required
@staff_required
@require_POST
def image_delete(request, pk):
    image = get_object_or_404(ProductImage, pk=pk)
    product_id = image.product_id
    image.delete()
    messages.info(request, "Imagem removida.")
    return redirect("dashboard:product_edit", pk=product_id)


# ---------------------------------------------------------------------------
# Categorias
# ---------------------------------------------------------------------------
@login_required
@staff_required
def category_list(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria criada.")
            return redirect("dashboard:category_list")
    else:
        form = CategoryForm()
    categories = Category.objects.annotate(product_count=Count("products"))
    return render(request, "dashboard/category_list.html", {
        "form": form,
        "active_categories": categories.filter(is_active=True),
        "inactive_categories": categories.filter(is_active=False),
        "active_count": categories.filter(is_active=True).count(),
    })


@login_required
@staff_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoria atualizada.")
            return redirect("dashboard:category_list")
    else:
        form = CategoryForm(instance=category)
    return render(request, "dashboard/category_form.html", {"form": form, "category": category})


@login_required
@staff_required
@require_POST
def category_toggle(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.is_active = not category.is_active
    category.save(update_fields=["is_active", "updated_at"])
    messages.success(
        request,
        f"Estilo \"{category.name}\" {'ativado' if category.is_active else 'desativado'}.",
    )
    return redirect(request.POST.get("next") or "dashboard:category_list")


@login_required
@staff_required
@require_POST
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if category.products.exists():
        messages.warning(request, "Não é possível excluir: há produtos nesta categoria.")
    else:
        category.delete()
        messages.info(request, "Categoria excluída.")
    return redirect("dashboard:category_list")


# ---------------------------------------------------------------------------
# Pedidos
# ---------------------------------------------------------------------------
@login_required
@staff_required
def order_list(request):
    query = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    orders = Order.objects.select_related("customer")
    if query:
        orders = orders.filter(
            Q(number__icontains=query)
            | Q(customer__name__icontains=query)
            | Q(customer__phone__icontains=query)
        )
    if status:
        orders = orders.filter(status=status)
    page = Paginator(orders, 20).get_page(request.GET.get("page"))
    return render(request, "dashboard/order_list.html", {
        "page_obj": page, "query": query, "status": status,
        "status_choices": OrderStatus.choices,
    })


@login_required
@staff_required
def order_detail(request, number):
    order = get_object_or_404(
        Order.objects.select_related("customer").prefetch_related("items", "history"),
        number=number,
    )
    return render(request, "dashboard/order_detail.html", {
        "order": order,
        "status_choices": OrderStatus.choices,
        "whatsapp_url": WhatsAppService.build_url(order, phone=order.customer.phone),
    })


@login_required
@staff_required
@require_POST
def order_change_status(request, number):
    order = get_object_or_404(Order, number=number)
    try:
        OrderService.change_status(order, request.POST.get("status"), request.POST.get("note", ""))
        messages.success(request, "Status atualizado.")
    except ValueError as exc:
        messages.warning(request, str(exc))
    return redirect("dashboard:order_detail", number=number)


# ---------------------------------------------------------------------------
# Clientes
# ---------------------------------------------------------------------------
@login_required
@staff_required
def customer_list(request):
    query = request.GET.get("q", "").strip()
    customers = Customer.objects.all()
    if query:
        customers = customers.filter(Q(name__icontains=query) | Q(phone__icontains=query))
    page = Paginator(customers, 20).get_page(request.GET.get("page"))
    return render(request, "dashboard/customer_list.html", {"page_obj": page, "query": query})


@login_required
@staff_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, "dashboard/customer_detail.html", {
        "customer": customer,
        "orders": customer.orders.all(),
    })


# ---------------------------------------------------------------------------
# Cupons
# ---------------------------------------------------------------------------
@login_required
@staff_required
def coupon_list(request):
    coupons = Coupon.objects.all()
    if request.method == "POST":
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cupom criado.")
            return redirect("dashboard:coupon_list")
    else:
        form = CouponForm()
    return render(request, "dashboard/coupon_list.html", {"coupons": coupons, "form": form})


@login_required
@staff_required
def coupon_edit(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    if request.method == "POST":
        form = CouponForm(request.POST, instance=coupon)
        if form.is_valid():
            form.save()
            messages.success(request, "Cupom atualizado.")
            return redirect("dashboard:coupon_list")
    else:
        form = CouponForm(instance=coupon)
    return render(request, "dashboard/coupon_form.html", {"form": form, "coupon": coupon})


@login_required
@staff_required
@require_POST
def coupon_toggle(request, pk):
    coupon = get_object_or_404(Coupon, pk=pk)
    coupon.is_active = not coupon.is_active
    coupon.save(update_fields=["is_active", "updated_at"])
    messages.success(request, "Cupom atualizado.")
    return redirect("dashboard:coupon_list")


# ---------------------------------------------------------------------------
# Avaliações
# ---------------------------------------------------------------------------
@login_required
@staff_required
def review_list(request):
    reviews = Review.objects.select_related("customer", "product").prefetch_related("images")
    page = Paginator(reviews, 20).get_page(request.GET.get("page"))
    return render(request, "dashboard/review_list.html", {"page_obj": page})


@login_required
@staff_required
@require_POST
def review_toggle(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.is_hidden = not review.is_hidden
    review.save(update_fields=["is_hidden", "updated_at"])
    messages.success(request, "Avaliação atualizada.")
    return redirect("dashboard:review_list")


@login_required
@staff_required
@require_POST
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    review.delete()
    messages.info(request, "Avaliação excluída.")
    return redirect("dashboard:review_list")
