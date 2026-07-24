import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='genyp').exists():
    User.objects.create_superuser('genyp', '', 'genyp123')
    print('Superusuário criado com sucesso!')
else:
    print('Superusuário já existe.')