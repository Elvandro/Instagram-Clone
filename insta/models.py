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

class Image(models.Model):
    image = models.ImageField(upload_to="images/")
    image_name = models.CharField(max_length=30, blank=True)
    image_caption = models.TextField(blank=True)
    profile_key = models.ForeignKey(Profile,on_delete=models.CASCADE)
    user_key = models.ForeignKey(User,on_delete= models.CASCADE)
    likes = models.PositiveIntegerField(defaul=0)

    def __str__(self):
        return self.image_name

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

    def update_caption(self,new_caption):
        self.image_caption = new_caption
        self.save()

    @classmethod
    def get_image_by_id(cls,id):
        retrived_image = Image.objects.get(id = id)
        return retrived_image

    @classmethod
    def get_images_by_user(cls,id):
        posted_images = Image.objects.filter(user_id=id)
        return posted_images                
