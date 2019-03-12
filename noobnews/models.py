from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.template.defaultfilters import slugify


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_profile_image = models.ImageField(
        default='NoProfile.jpg', upload_to='static/profile_images')
    # image = models.ImageField(default='default.jpg',
    # upload_to = 'static/profile_images')
    player_tag = models.CharField(max_length=128, unique=True)
    # image=models.ImageField(
    # upload_to='static/profile_images', blank=True, default='profile_images/default-user.png')

<<<<<<< HEAD
    def __str__(self):
=======
    def _str_(self):
>>>>>>> 0377badc90e4f54fca25e3e1fb36df54f1882129
        return f'{self.user.username}'


class Genre(models.Model):
    genre_id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=128)

    def _str_(self):
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
<<<<<<< HEAD
    trivia = models.CharField(max_length=300, default="There are no Trivia available for this game at the moment")
    cheats = models.CharField(max_length=300, default="There are no Cheats available for this game at the moment")
    easter_eggs = models.CharField(max_length=300, default="There are no Easter Eggs available for this game at the moment")
=======
    trivia = models.CharField(max_length=300)
>>>>>>> 0377badc90e4f54fca25e3e1fb36df54f1882129

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(VideoGame, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'videogames'

    def _str_(self):
        return self.name


class Review(models.Model):
    reviews_id = models.IntegerField(unique=True, primary_key=True)
    videogame = models.ForeignKey(VideoGame)
    user_id = models.ForeignKey(UserProfile)
    comments = models.CharField(max_length=300)
    publish_date = models.DateField(("Date"), default=date.today)
    comment_rating = models.IntegerField(default=0)

<<<<<<< HEAD
    def __str__(self):
=======
    def _str_(self):
>>>>>>> 0377badc90e4f54fca25e3e1fb36df54f1882129
        return self.videogame.name


class VideoGameList(models.Model):
    list_id = models.IntegerField(unique=True, primary_key=True)
    videogame_id = models.ForeignKey(VideoGame)
    user_id = models.ForeignKey(UserProfile)

    def _str_(self):
        return self.list_id

<<<<<<< HEAD
class VideoExtraInfo(models.Model):
    videogame_id = models.ForeignKey(VideoGame)

    def __str__(self):
        return self.trivia
=======
# class VideoExtraInfo(models.Model):
#     videogame_id = models.ForeignKey(VideoGame)
#     trivia = models.CharField(max_length=300, default="There is no Trivia available for this game at the moment")
#     cheats = models.CharField(max_length=300, default="There is no Cheats available for this game at the moment")
#     credits = models.CharField(max_length=300, default="There is no Credits available for this game at the moment")
#     triviaPicture = models.CharField(max_length=300, default="There is no Trivia available for this game at the moment")
#     cheatPicture = models.CharField(max_length=300, default="There is no Cheats available for this game at the moment")
#     creditPicture = models.CharField(max_length=300, default="There is no Credits available for this game at the moment")
#
#     def __str__(self):
#         return self.trivia
>>>>>>> 0377badc90e4f54fca25e3e1fb36df54f1882129

class ratingValue(models.Model):
    number = models.IntegerField(default=0)
    value = models.FloatField(default=0)

<<<<<<< HEAD
    def __str__(self):
=======
    def __int__(self):
>>>>>>> 0377badc90e4f54fca25e3e1fb36df54f1882129
        return self.number

class score(models.Model):
    videogame = models.ForeignKey(VideoGame)
    score = models.FloatField(default=0)

<<<<<<< HEAD
    def __str__(self):
=======
    def __int__(self):
>>>>>>> 0377badc90e4f54fca25e3e1fb36df54f1882129
        return self.videogame
