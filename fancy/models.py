from django.db.models import Model, DateTimeField
from django.utils import timezone


class SafeDeleteModel(Model):
    deleted_at = DateTimeField(null=True, db_index=True)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()


class LogFieldsModel(Model):
    inserted_at = DateTimeField(auto_now_add=True, db_index=True)
    updated_at = DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
