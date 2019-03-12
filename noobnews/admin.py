from django.contrib import admin
<<<<<<< HEAD
from noobnews.models import UserProfile, Genre, VideoGame, Review, VideoGameList, ratingValue
=======
from noobnews.models import UserProfile, Genre, VideoGame, Review, VideoGameList,score,ratingValue
>>>>>>> 0377badc90e4f54fca25e3e1fb36df54f1882129
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
<<<<<<< HEAD
=======
admin.site.register(score)
>>>>>>> 0377badc90e4f54fca25e3e1fb36df54f1882129
