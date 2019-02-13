from django.contrib import admin
from noobnews.models import User, Genre, VideoGame, Review, VideoGameList
# Register your models here.

admin.site.register(User)
admin.site.register(Genre)
admin.site.register(VideoGame)
admin.site.register(Review)
admin.site.register(VideoGameList)
