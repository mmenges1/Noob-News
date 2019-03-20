from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models.signals import pre_save, post_save, m2m_changed


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Default images
    user_profile_image = models.ImageField(
        default='NoProfile.jpg', upload_to='static/profile_images')
    game_library_image = models.ImageField(
        default='default_videogame.jpg', upload_to='static/video_game_default')
    player_tag = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return f'{self.user.username}'


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
    description = models.CharField(max_length=1000)
    rating = models.IntegerField(default=0)
    release = models.DateField(("Date"), default=date.today)
    developer = models.CharField(max_length=128)
    publisher = models.CharField(max_length=128)
    image = models.ImageField(default="")
    youtubeurl = models.CharField(max_length=300)
    speedRun = models.CharField(max_length=300)
    trivia = models.CharField(
        max_length=300, default="There are no Trivia available for this game at the moment")
    cheats = models.CharField(
        max_length=300, default="There are no Cheats available for this game at the moment")
    easter_eggs = models.CharField(
        max_length=300, default="There are no Easter Eggs available for this game at the moment")

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
    comment_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.videogame.name


# Manage library
class VideoGameListManager(models.Manager):

    def new_or_get(self, request):
        library_id = request.session.get("library_id", None)
        qs = self.get_queryset().filter(list_id=library_id)

        if qs.count() == 1:
            new_obj = False
            library_obj = qs.first()
            if request.user.is_authenticated() and library_obj.user is None:
                library_obj.user = request.user
                library_obj.save()
        else:
            user = request.user.userprofile
            library_obj = VideoGameList.objects.new(
                user=request.user.userprofile)
            new_obj = True
            request.session['library_id'] = library_obj.list_id
        return library_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            user_obj = user
        return self.model.objects.create(user=user_obj)

# Make a library for favorite games


class VideoGameList(models.Model):
    list_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, null=True)
    userLibrary = models.ManyToManyField(VideoGame, blank=True)
    game_library_image = models.ImageField(
        default='default_videogame.jpg', upload_to='static/video_game_default')

    objects = VideoGameListManager()

    def __str__(self):
        return str(self.list_id)


def m2m_changed_video_game_list(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        userLibrary = instance.userLibrary.all()
        instance.save()


m2m_changed.connect(m2m_changed_video_game_list,
                    sender=VideoGameList.userLibrary.through)


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

class ratingValue(models.Model):
    number = models.IntegerField(default=0)
    value = models.FloatField(default=0)

    def __str__(self):
        return self.number


class score(models.Model):
    videogame = models.ForeignKey(VideoGame)
    score = models.FloatField(default=0)

    def __str__(self):
        return self.videogame
