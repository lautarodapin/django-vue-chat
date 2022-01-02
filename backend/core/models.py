from django.db import models
from django.contrib.auth import get_user_model

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    mod_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(get_user_model(), models.SET_NULL, related_name='+', null=True, blank=True)
    mod_by = models.ForeignKey(get_user_model(), models.SET_NULL, related_name='+', null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']