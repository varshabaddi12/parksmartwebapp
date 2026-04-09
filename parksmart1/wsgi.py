"""
WSGI config for parksmart project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parksmart1.settings')

application = get_wsgi_application()

from django.contrib.auth import get_user_model
from .models import Slot  # Ensure 'Slot' is the name in your models.py

try:
    # 1. Ensure Admin exists
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

    # 2. Automatically create 1200 slots if the database is empty
    if Slot.objects.count() == 0:
        # Configuration: (Type, Count, Prefix)
        configs = [
            ('4-wheeler', 400, 'CAR'),
            ('2-wheeler', 500, 'BIKE'),
            ('3-wheeler', 300, 'AUTO')
        ]
        
        for v_type, count, prefix in configs:
            slots_to_create = []
            for i in range(1, count + 1):
                slots_to_create.append(
                    Slot(
                        slot_name=f"{prefix}-{i}", 
                        vehicle_type=v_type, 
                        is_available=True
                    )
                )
            # This creates them all at once (very fast)
            Slot.objects.bulk_create(slots_to_create)
            
        print("Successfully created 1200 parking slots!")
except Exception as e:
    print(f"Error during auto-setup: {e}")