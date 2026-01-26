import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "buildstock.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "test"
email = "test@example.com"
password = "Test@2026"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser '{username}' créé avec succès.")
else:
    print(f"Superuser '{username}' existe déjà.")