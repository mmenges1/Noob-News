def create_user():
    # Create a user
    from noobnews.models import User, UserProfile
    user = User.objects.get_or_create(username="testuser@testuser.com", password="test1234",
                                      first_name="Test", last_name="User", email="testuser@testuser.com")[0]
    user.set_password(user.password)
    user.save()

    # Create a user profile
    user_profile = UserProfile.objects.get_or_create(user=user,
                                                     player_tag="test_user")[0]
    user_profile.save()

    return user, user_profile


def create_videogame(image=None):
    from noobnews.models import VideoGame, Genre
    import datetime
    genre = Genre.objects.create(genre_id=1, name="Adventure")
    genre.save()

    videogame = VideoGame.objects.create(id=56,
                                         name="S.C.A.R.S.",
                                         genre=genre,
                                         description="Is a racing video game featuring cars that are shaped like animals. It was released on the Nintendo 64, PlayStation and for Microsoft Windows.",
                                         rating=4,
                                         release=datetime.date(
                                             1998, 9, 30),
                                         developer="Vivid Image",
                                         publisher="Ubisoft")
    if image:
        videogame.image = image

    videogame.save()

    return videogame


def create_videogames_library(user_profile, videogame):
    from noobnews.models import VideoGameList
    videogame_list = VideoGameList.objects.create(user=user_profile)
    videogame_list.userLibrary.add(videogame)

    videogame_list.save()

    return videogame_list


def create_review(user_profile, videogame):
    from noobnews.models import Review
    import datetime
    review = Review.objects.create(comments='Test comment', comment_rating=3,
                                   videogame=videogame, publish_date=str(datetime.date.today()), user_id=user_profile)
    return review
