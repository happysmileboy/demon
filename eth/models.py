from django.db import models
from django.conf import settings
from pywallet.wallet import HDPrivateKey, HDKey
from pywallet import wallet
# Create your models here.


class Admin_wallet(models.Model):
    seed = models.TextField()
    coin = models.TextField()
    xpub = models.TextField()
    xpriv = models.TextField()
    address = models.TextField()


class Wallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        Admin_wallet,
        related_name='wallet',
        on_delete=models.CASCADE,
    )
    address = models.TextField()
    private_key = models.TextField()
    value = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

