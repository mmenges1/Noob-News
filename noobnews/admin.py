from django.contrib import admin
from noobnews.models import User, Genre, VideoGame, Review, VideoGameList
# Register your models here.

class VideoGameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


admin.site.register(User)
admin.site.register(Genre)
admin.site.register(VideoGame, VideoGameAdmin)
admin.site.register(Review)
admin.site.register(VideoGameList)
