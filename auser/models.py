from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class CustomUserChannel(models.Model):
    owner = models.OneToOneField(to=CustomUser, on_delete=models.CASCADE, related_name="channel_user")
    name = models.CharField(max_length=255, null=True, blank=True)
    describe = models.TextField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.owner.get_full_name()
        super().save(*args, **kwargs)

    def __str__(self):
        # return self.name
        return str(self.pk)
