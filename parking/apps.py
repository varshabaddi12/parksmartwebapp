from django.apps import AppConfig

class parksmartwebappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'parking'

    def ready(self):
        # This function runs as soon as Django starts
        from django.contrib.auth import get_user_model
        
        try:
            # 1. Create the Admin account automatically
            User = get_user_model()
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser('admin', 'admin@example.com', 'admin123')

            # 2. Create the 1,200 slots automatically if the DB is empty
            from .models import Slot 
            if Slot.objects.count() == 0:
                configs = [
                    ('4-wheeler', 400, 'CAR'),
                    ('2-wheeler', 500, 'BIKE'),
                    ('3-wheeler', 300, 'AUTO')
                ]
                slots_to_create = []
                for v_type, count, prefix in configs:
                    for i in range(1, count + 1):
                        slots_to_create.append(
                            Slot(slot_name=f"{prefix}-{i}", vehicle_type=v_type, is_available=True)
                        )
                Slot.objects.bulk_create(slots_to_create)
        except Exception:
            # This ensures the site doesn't crash during the first setup
            pass