from django.db import models
from django.contrib.auth.models import User
import datetime as dt

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_name = models.CharField(max_length=30, default='User')
    profile_photo = models.ImageField(upload_to="profiles/")
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.profile_name

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profiles(cls):
        profiles = cls.objects.all()
        return profiles

    @classmethod
    def find_profile(cls, query):
        profile = cls.objects.filter(profile_name__icontains = query).all()
        return profile

class Image(models.Model):
    image = models.ImageField(upload_to="images/")
    image_name = models.CharField(max_length=30, blank=True)
    image_caption = models.TextField(blank=True)
    profile_key = models.ForeignKey(Profile,on_delete=models.CASCADE)
    user_key = models.ForeignKey(User,on_delete= models.CASCADE)
    likes = models.PositiveIntegerField(default=0)
    pub_date = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-pub_date']

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

class Comment(models.Model):
    comment = models.TextField(blank=True)
    date_posted = models.DateTimeField(auto_now_add=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return self.comment

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()


class Friend(models.Model):
    users = models.ManyToManyField(User)
    current_user = models.ForeignKey(User, related_name='owner', null=True)

    @classmethod
    def make_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.users.add(new_friend)

    @classmethod
    def lose_friend(cls, current_user, new_friend):
        friend, created = cls.objects.get_or_create(current_user=current_user)
        friend.users.remove(new_friend)
