"""Cria (ou atualiza) o usuário administrador do painel.

Comando idempotente: pode rodar em todo deploy sem duplicar usuários.
Se o usuário já existir, apenas garante a senha e as permissões de staff.

Uso:
    python manage.py criar_admin

Os valores padrão podem ser sobrescritos por variáveis de ambiente:
    ADMIN_USERNAME, ADMIN_PASSWORD, ADMIN_EMAIL
"""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Cria ou atualiza o usuário administrador do painel King Street."

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.getenv("ADMIN_USERNAME", "emerson").strip()
        password = os.getenv("ADMIN_PASSWORD", "emer123")
        email = os.getenv("ADMIN_EMAIL", "emerson@kingstreet.local").strip()

        user, criado = User.objects.get_or_create(
            username=username,
            defaults={"email": email, "is_staff": True, "is_superuser": True},
        )

        # Garante senha e permissões mesmo se o usuário já existia.
        user.email = email or user.email
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save()

        acao = "criado" if criado else "atualizado"
        self.stdout.write(
            self.style.SUCCESS(f"Administrador '{username}' {acao} com sucesso.")
        )
