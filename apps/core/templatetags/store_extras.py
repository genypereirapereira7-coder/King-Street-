from decimal import Decimal, InvalidOperation

from django import template

register = template.Library()


@register.filter
def brl(value):
    """Formata um valor como moeda brasileira: 1234.5 -> R$ 1.234,50."""
    try:
        value = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError):
        return "R$ 0,00"
    inteiro, _, centavos = f"{value:.2f}".partition(".")
    negativo = inteiro.startswith("-")
    inteiro = inteiro.lstrip("-")
    partes = []
    while len(inteiro) > 3:
        partes.insert(0, inteiro[-3:])
        inteiro = inteiro[:-3]
    partes.insert(0, inteiro)
    formatado = ".".join(partes)
    sinal = "-" if negativo else ""
    return f"R$ {sinal}{formatado},{centavos}"


@register.filter
def stars(value):
    """Retorna a nota como estrelas cheias e vazias."""
    try:
        n = int(value)
    except (TypeError, ValueError):
        n = 0
    n = max(0, min(5, n))
    return "★" * n + "☆" * (5 - n)
