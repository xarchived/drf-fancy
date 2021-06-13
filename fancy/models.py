from django.db import models
from django.utils import timezone


class SafeDeleteModel(models.Model):
    deleted_at = models.DateTimeField(null=True, db_index=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()


class LogFieldsModel(models.Model):
    inserted_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
