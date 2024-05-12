from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _


class BaseModel(models.Model):
    def get_admin(self):
        user = User.objects.get(username='admin')
        return user

    # TODO
    def save(self, *args, **kwargs):
        self.x_user = self.get_admin()
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


class EashoUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="easho_user")
    prefix = models.CharField(_("Prefix"), max_length=8, blank=True)
