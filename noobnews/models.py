from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.template.defaultfilters import slugify


# Create your models here.

# class UserProfile(models.Model):
#   user = models.OneToOneField(User)
#  player_tag = models.CharField(max_length=128, unique=True)
# user_profile_image = models.ImageField(
#    upload_to='static/profile_images', blank=True, default='profile_images/default-user.png')

# def __str__(self):
#   return self.player_tag

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_profile_image = models.ImageField(default='NoProfile.jpg', upload_to='profile_pics')
    # image = models.ImageField(default='default.jpg',
    # upload_to = 'static/profile_images')
    player_tag = models.CharField(max_length=128, unique=True)
    # image=models.ImageField(
    # upload_to='static/profile_images', blank=True, default='profile_images/default-user.png')

    def __str__(self):
       # return self.player_tag
        return f'{self.user.username} Profile'


class Genre(models.Model):
    genre_id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class VideoGame(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    genre = models.ForeignKey(Genre)
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(blank=True)
    description = models.CharField(max_length=300)
    rating = models.IntegerField(default=0)
    release = models.DateField(("Date"), default=date.today)
    developer = models.CharField(max_length=128)
    publisher = models.CharField(max_length=128)
    image = models.ImageField(default="")
    youtubeurl = models.CharField(max_length=300)
    speedRun = models.CharField(max_length=300)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(VideoGame, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'videogames'

    def __str__(self):
        return self.name


class Review(models.Model):
    reviews_id = models.IntegerField(unique=True, primary_key=True)
    videogame = models.ForeignKey(VideoGame)
    user_id = models.ForeignKey(UserProfile)
    comments = models.CharField(max_length=300)
    publish_date = models.DateField(("Date"), default=date.today)
    rating = models.IntegerField(default=0)

    def __int__(self):
        return self.reviews_id


class VideoGameList(models.Model):
    list_id = models.IntegerField(unique=True, primary_key=True)
    videogame_id = models.ForeignKey(VideoGame)
    user_id = models.ForeignKey(UserProfile)

    def __str__(self):
        return self.list_id


# class Profile(models.Model):
 #   user = models.OneToOneField(User, on_delete=models.CASCADE)
  #  image = models.ImageField(default='default.jpg', upload_to='profile_pics')

   # def __str__(self):
    #    return f'{self.user.username} Profile'
