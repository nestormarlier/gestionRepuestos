# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Stock, StockAudit

@receiver(post_save, sender=Stock)
def save_stock_audit(sender, instance, created, **kwargs):
    user = instance.modified_by  # Asume que tienes un campo 'modified_by' en el modelo Stock para registrar el usuario
    action = 'Creado' if created else 'Actualizado'
    StockAudit.objects.create(stock=instance, user=user, action=action, cantidad=instance.stock_real)