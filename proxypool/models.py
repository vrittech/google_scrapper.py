from django.db import models
from accounts.models import CustomUser

class ProxyPool(models.Model):
    ip_address = models.GenericIPAddressField()
    port = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.ip_address}:{self.port} - {'Active' if self.is_active else 'Inactive'}"


class UserProxyAssignment(models.Model):
    """
    Tracks proxy assignments for users.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='proxy_assignment')
    proxies = models.ManyToManyField(ProxyPool, related_name='assigned_users')
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proxy Assignment for {self.user.username}"
