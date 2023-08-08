from django.db import models

from users.models import User


class Fund(models.Model):
    # TODO: Change the on_delete action to SET_NULL after testing
    user = models.ForeignKey(User, name="provider", on_delete=models.CASCADE, related_name="user_funds")

    class Meta:
        db_table = "funds"
        verbose_name = "fund"
        verbose_name_plural = "funds"
