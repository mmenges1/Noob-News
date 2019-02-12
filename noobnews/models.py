from django.db import models
from datetime import date

# Create your models here.

class User(models.Model):
    user_id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=128)
    player_tag = models.CharField(max_length=128, unique=True)
    email =  models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=128)
    profile_image = models.CharField(max_length=300)

    def __str__(self):
        return self.player_tag

class Genre(models.Model):
    genre_id = models.IntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class VideoGame(models.Model):
    id = models.IntegerField(unique=True, primary_key=True)
    genre = models.ForeignKey(Genre)
    name = models.CharField(max_length=128)
    description = models.CharField(max_length=300)
    rating = models.IntegerField(default=0)
    release = models.DateField(("Date"),default=date.today)
    developer = models.CharField(max_length=128)
    publisher = models.CharField(max_length=128)
    image = models.CharField(max_length=300)


    def __str__(self):
        return self.name

class Review(models.Model):
    reviews_id = models.IntegerField(unique=True, primary_key=True)
    videogame = models.ForeignKey(VideoGame)
    user_id = models.ForeignKey(User)
    comments =  models.CharField(max_length=300)
    publish_date = models.DateField(("Date"),default=date.today)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.reviews_id

class VideoGameList(models.Model):
    list_id = models.IntegerField(unique=True, primary_key=True)
    videogame_id = models.ForeignKey(VideoGame)
    user_id = models.ForeignKey(User)

    def __str__(self):
        return self.list_id
