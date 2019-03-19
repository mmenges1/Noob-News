from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.core.urlresolvers import reverse
from noobnews.models import VideoGame, VideoGameList, Genre, ratingValue, User, UserProfile, Review
import noobnews.test_utils as test_utils
import populate_noobnews
import datetime
import os

# Check if both arrays are equal


def checkEqualArray(arr1, arr2):
    return len(arr1) == len(arr2) and sorted(arr1) == sorted(arr2)


class PopulationScriptTests(TestCase):
    # Check if all the data is populated in the database
    def test_right_amount_data(self):
        # Populate database
        populate_noobnews.populate()
        # Get the number of videogames from the database
        number_videogames = VideoGame.objects.count()
        self.assertGreaterEqual(55, number_videogames)
        # Get the number of genres from the database
        number_genres = Genre.objects.count()
        self.assertGreaterEqual(5, number_genres)
        # Get the number of rating values from the database
        number_rating_values = ratingValue.objects.count()
        self.assertEqual(5, number_rating_values)
        # Get the number of user profiles from the database
        number_user_profiles = UserProfile.objects.count()
        self.assertGreaterEqual(7, number_user_profiles)
        # Get the number of reviews from the database
        number_reviews = Review.objects.count()
        self.assertGreaterEqual(64, number_reviews)

    def test_right_values_data(self):
        # Populate database
        populate_noobnews.populate()
        # Get a videogame to check if it has the correct values
        videogame = VideoGame.objects.get(name="Uncharted 4: A Thief's End")
        self.assertEqual(videogame.id, 8)
        self.assertEqual(videogame.genre.genre_id, 2000)
        self.assertEqual(videogame.rating, 5)
        self.assertEqual(videogame.release, datetime.date(2016, 5, 10))
        self.assertEqual(videogame.developer, "Naughty Dog")
        self.assertEqual(videogame.publisher, "Sony Computer Entertainment")
        self.assertEqual(
            videogame.image, "/static/videogameImages/uncharted4.jpg")
        # Get the rating values to check if they are correct
        rating_values = ratingValue.objects.all().values_list(flat=True)
        self.assertEqual(checkEqualArray(rating_values, [1, 2, 3, 4, 5]), True)

    def test_data_insertion(self):

        # Create a user
        user, user_profile = test_utils.create_user()

        # Check there is only the saved user and its profile in the database
        all_users = User.objects.all()
        self.assertEquals(len(all_users), 1)

        all_profiles = UserProfile.objects.all()
        self.assertEquals(len(all_profiles), 1)

        # Check profile fields were saved correctly
        all_profiles[0].user = user
        all_profiles[0].player_tag = user_profile.player_tag

        # Create a videogame
        videogame = test_utils.create_videogame()

        # Check there is only the saved videogame
        all_videogames = VideoGame.objects.all()
        self.assertEquals(len(all_videogames), 1)

        # Check if the videogames library is created successfully
        videogame_list = test_utils.create_videogames_library(
            all_profiles[0], videogame)

        # Check there is only one videogame in the videogames library
        user_videogames = videogame_list.userLibrary.all()
        self.assertEquals(len(user_videogames), 1)

        #Check if the review is created successfully
        review=test_utils.create_review(all_profiles[0], videogame)

        #Check the is only one review for the videogame
        reviews = Review.objects.all()
        self.assertEquals(len(reviews), 1)

    def test_upload_image(self):
        # Create fake user and image to upload to register user
        image = SimpleUploadedFile(
            "testvideogame.jpg", b"file_content", content_type="image/jpeg")
        videogame = test_utils.create_videogame(image)
        videogame = VideoGame.objects.get(id=56)
        path_to_image = './media/testvideogame.jpg'

        # Check file was saved properly
        self.assertTrue(os.path.isfile(path_to_image))

        # Delete fake file created
        os.remove(path_to_image)


class NavigationTests(TestCase):
    def test_login_redirects_to_profile(self):
        # Create a user
        user, user_profile = test_utils.create_user()
        videogame = test_utils.create_videogame()
        videogame_list = test_utils.create_videogames_library(
            user_profile, videogame)

        # Access login page via POST with user data
        try:
            response = self.client.post(
                reverse('login'), {'mail': 'testuser@testuser.com', 'password': 'test1234'}, follow=True)
        except Exception as e:
            self.assertTrue(False)

        # Check it redirects to profile
        self.assertRedirects(response, reverse('profile'))

    def test_home_redirects_to_videogame(self):
        # Populate database
        populate_noobnews.populate()

        # Access videogame page via GET with videogame data
        try:
            response = self.client.get(
                reverse('show_videogame', kwargs={'videogame_name_slug': 'spider-man'}))
        except Exception as e:
            self.assertTrue(False)

        # Check it get the correct data for the videogame Spider-Man
        self.assertIn('the super-human crime lord Mr. Negative orchestrates a plot to seize control of New York City'.lower(),
                      response.content.decode('ascii').lower())
