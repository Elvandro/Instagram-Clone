from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    profile_name = models.CharField(default='User')
    profile_photo = models.ImageField(upload_to="profiles/")
    bio = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.profile_name

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def find_profile(cls, query):
        found_profiles = cls.objects.filter(profile_name__icontains = query).all()
        return found_profiles            
