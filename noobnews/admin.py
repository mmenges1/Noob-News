from django.contrib import admin
from noobnews.models import UserProfile, Genre, VideoGame, Review, VideoGameList,score,ratingValue
#from .models import Profile
# Register your models here.


class VideoGameAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(UserProfile)
admin.site.register(Genre)
admin.site.register(VideoGame, VideoGameAdmin)
admin.site.register(Review)
admin.site.register(VideoGameList)
admin.site.register(ratingValue)
admin.site.register(score)
