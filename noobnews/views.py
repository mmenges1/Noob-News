from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from email.mime.image import MIMEImage
from django.contrib.auth import logout
from django.template import loader
from django.contrib import messages
from datetime import datetime
from noobnews.models import VideoGame, Genre, Review, User, UserProfile, VideoGameList
from noobnews.forms import UserForm, UserProfileForm, ReviewForm, PasswordResetRequestForm, SetPasswordForm, ContactForm, VideoImageUpdateForm
from datetime import date
from social_django.models import UserSocialAuth
from django.db.models import Max
from django.views.generic import DetailView
from noobnews.models import VideoGame, Genre, Review, User, UserProfile, ratingValue, score
from noobnews.forms import UserForm, UserProfileForm, ReviewForm, PasswordResetRequestForm, SetPasswordForm, ContactForm, SuggestForm
from datetime import date
from social_django.models import UserSocialAuth
from django.db.models import Max
import os
import random
from django.db.models import Count
from django.db.models import Sum

from django.db.models.signals import pre_save, post_save, m2m_changed

from noobnews.forms import ProfileUpdateForm, UserUpdateForm


def home(request):
    top40List = VideoGame.objects.order_by('-rating')[:40]
    top1 = get_random()
    top2 = get_random()
    top3 = get_random()
    stream = get_random_stream()
    context_dict = {
        'top1': top1,
        'top2': top2,
        'top3': top3,
        'stream': stream,
        'top40List': top40List,
        'user': request.user
    }
    return render(request, 'noobnews/home.html', context_dict)


def get_random():
    max_id = VideoGame.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        videogame = VideoGame.objects.filter(pk=pk).first()
        if videogame:
            return videogame


def get_random_stream():
    max_id = VideoGame.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        videogame = VideoGame.objects.filter(pk=pk).first()
        if videogame:
            return videogame


def profile(request):
    return render(request, 'noobnews/profile.php')


def show_videogame(request, videogame_name_slug):
    context_dict = {}
    form = ReviewForm()

    try:
        videoGame = VideoGame.objects.get(slug=videogame_name_slug)
        genres = Review.objects.filter(videogame=videoGame)
        users = UserProfile.objects.all()
        context_dict = {'users': users,
                        'genres': genres, 'videoGame': videoGame}
    except:
        videoGame = None
        videoGame_name_slug = None
        context_dict['videoGame'] = None
        context_dict['genres'] = None
        context_dict['users'] = None
    # ********* Working out the Value of each review ***********
    # Explication on rating system- Work out the total numner of reviews currently stored and divide 5- this will give us a base rating
    # Next we need to multiple the base rating with each of the ratings- (1,2,3,4,5) as this will allow us to see how much each of these ratings are worth (these need to be stored in the database)
    # Then using this we can count how many 1 star, 2 star etc reviews that each game have and multiple by how much the rating is worth,
    # We add these reviews all together to give us a over all game score
    # Next we get the Review with the higest score and we work out the percentage the other games are of that score- this means all of the games will have a number between 1 and 100


    # Gets the total number of reviews and works out out base rating
    totalRating = Review.objects.all().aggregate(Sum('comment_rating'))[
        'comment_rating__sum'] or 0.00
    totalRating = totalRating/5

    # Need to delete all objects in the score table
    score.objects.all().delete()

    # updating the rating table with the new rating values
    for i in range(1, 6):
        rat = totalRating * i
        updaterating = ratingValue.objects.filter(number=i)
        updaterating = updaterating[0]
        updaterating.value = rat
        updaterating.save()

    ratingVideoGames = VideoGame.objects.all()

    size = len(ratingVideoGames)
    # Gets the game score based on the number of differnt stars reviews the game has
    for j in range(size):
        currentgame = ratingVideoGames[j]
        Gamescore = 0

        for k in range(1, 6):
            currentReview = Review.objects.filter(videogame=currentgame, comment_rating=k)
            currentValue = ratingValue.objects.filter(number=k)
            currentscore = currentValue[0].value * len(currentReview)
            Gamescore = Gamescore + currentscore

            # need to update score table with these value
        score.objects.create(videogame=currentgame, score=Gamescore)

        # Need to find the highest Score
    highestScore = score.objects.all().aggregate(Max('score'))[
        'score__max'] or 0.00

    for l in range(size):
        # Works out what percentage that the game score is compared to the higest game, this is the rating
        currentgame = ratingVideoGames[l]
        currentScore = score.objects.filter(videogame=currentgame)
        currentScore = currentScore[0].score
        gameScore = currentScore / highestScore
        gameScore = gameScore * 100
        updateGame = VideoGame.objects.filter(name=currentgame.name)
        updateGame = updateGame[0]
        updateGame.rating = gameScore

        # Stores the new rating in the database
        updateGame.save()

    # A HTTP POST?
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        print(form)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            if videoGame:
                review = form.save(commit=False)
                review.videogame = videoGame
                review.publish_date = str(date.today())
                print(request.user)
                review.user_id = UserProfile.objects.get(
                    player_tag=request.user.userprofile.player_tag)
                review.save()
                # return show_videogame(request, videogame_name_slug)

    context_dict['form'] = form
    context_dict['videogame'] = videoGame

    return render(request, 'noobnews/videogame.html', context_dict)


def suggestChanges(request, videogame_name_slug):
    context_dict = {}
    form = SuggestForm()

    try:
        videoGame = VideoGame.objects.get(slug=videogame_name_slug)
        # genres = Review.objects.filter(videogame=videoGame)
        users = UserProfile.objects.all()
        context_dict = {'users': users, 'videoGame': videoGame}
    except:
        videoGame = None
        videoGame_name_slug = None
        context_dict['videoGame'] = None
        context_dict['genres'] = None
        context_dict['users'] = None

    # A HTTP POST?
    if request.method == 'POST':
        form = SuggestForm(request.POST, instance=videoGame)
        # Have we been provided with a valid form?
        if form.is_valid():
            if videoGame:
                form.save()
            return render(request, 'noobnews/videogame.html', context_dict)
        print(form)
        # return show_videogame(request, videogame_name_slug)
    return render(request, 'noobnews/videogameSuggestChanges.html', context_dict)


def top40(request):
    context_dict = {}
    try:
        genres = Genre.objects.all()
        videoGame = VideoGame.objects.order_by('-rating')[:40]
        context_dict['genres'] = genres
        context_dict['videoGame'] = videoGame
    except VideoGame.DoesNotExist:
        context_dict['genres'] = None
        context_dict['videoGame'] = None

    return render(request, 'noobnews/top40.html', context_dict)


def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = VideoGame.objects.filter(name__contains=starts_with)
    if max_results > 0:
        if len(cat_list) > max_results:
            cat_list = cat_list[:max_results]
    return cat_list


def suggest_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    cat_list = get_category_list(8, starts_with)
    return render(request, 'noobnews/cats.html', {'cats': cat_list})

# Method to login


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('mail')
        password = request.POST.get('password')
        # using the django authentication framework to manage the login process
        user = authenticate(username=email, password=password)
        # If the credentials are correct
        if user:
            # If the user is active
            if user.is_active:
                # process the authenticated user to store session keys
                login(request, user)
                # Redirect to the profile page
                return HttpResponseRedirect(reverse('profile'))
            else:
                return HttpResponse("Your account is disabled")
        else:
            # Message to show the user if the credentials are wrong
            message = "Invalid login details"
            messages.error(request, message)
            return render(request, 'noobnews/login.html', {'message': message})

    else:
        return render(request, 'noobnews/login.html', {})

# Method to register a new user


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            repeat_password = user_form.cleaned_data['repeat_password']
            # Validate that both passwords match
            if(user_form.cleaned_data['password'] != repeat_password):
                messages.error(request, 'The passwords do not match!')
                return render(request,
                              'noobnews/register.html',
                              {
                                  'user_form': user_form,
                                  'profile_form': profile_form,
                              })
            try:
                # Search for a user with the same email that we are trying to register
                userTmp = User.objects.get(
                    email=user_form.cleaned_data['email'])
            except User.DoesNotExist:
                userTmp = None

            if userTmp:
                # If a user exists, notify the user about the error
                messages.error(request, 'A user with the email ' +
                               userTmp.email+' already exists')
                return render(request,
                              'noobnews/register.html',
                              {
                                  'user_form': user_form,
                                  'profile_form': profile_form,
                                  'registered': registered
                              })

            try:
                # Search for a user profile with the same player_tag that we are trying to register
                profileTmp = UserProfile.objects.get(
                    player_tag=profile_form.cleaned_data['player_tag'])
            except UserProfile.DoesNotExist:
                profileTmp = None

            if profileTmp:
                # If a user profile exists, notify the user
                messages.error(request, 'A user with the player tag ' +
                               profileTmp.player_tag+' already exists')
                return render(request,
                              'noobnews/register.html',
                              {
                                  'user_form': user_form,
                                  'profile_form': profile_form,
                                  'registered': registered
                              })
            # Store the user data from the form without save it in the databse
            user = user_form.save(commit=False)
            user.set_password(user.password)
            # Store the user profile data from the form without save it in the databse
            profile = profile_form.save(commit=False)
            # Set the username as the email for authentication purposes
            user.username = user.email
            # Save the user in the database
            user.save()
            profile.user = user
            # If the user uploaded a profile image
            if 'user_profile_image' in request.FILES:
                profile.user_profile_image = request.FILES['user_profile_image']

            profile.save()
            registered = True
            messages.success(request, 'Account created successfully!')
            return HttpResponseRedirect(reverse('login'))
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'noobnews/register.html',
                  {
                      'user_form': user_form,
                      'profile_form': profile_form,
                      'registered': registered
                  })

# Method to reset the password using the django authentication framwework


def reset_password(request):
    if request.method == 'POST':
        # Store the form information
        reset_form = PasswordResetRequestForm(data=request.POST)
        if reset_form.is_valid():
            userTmp = None
            profileTmp = None
            # The user is allowed to type the email or the player tag to reset the password
            data = reset_form.cleaned_data["email_or_playertag"]
            try:
                # Validation to check if the user typed the email
                validate_email(data)
                is_email = True
            except ValidationError:
                is_email = False

            if is_email is True:
                try:
                    # Search the user by email
                    userTmp = User.objects.get(email=data)
                except User.DoesNotExist:
                    userTmp = None
            else:
                try:
                    # Search the user profile by player tag
                    profileTmp = UserProfile.objects.get(player_tag=data)
                except UserProfile.DoesNotExist:
                    profileTmp = None

            if userTmp is None and profileTmp is None:
                # If there is no record for the input data, show the error to the user
                messages.error(
                    request, 'Sorry, we do not have any user associated with the information provided')
                return render(request,
                              'noobnews/password_reset_form.html',
                              {
                                  'reset_form': reset_form
                              })
            if profileTmp:
                userTmp = profileTmp.user
            # Directory to set the required variables to the password_reset_email.html template
            blend_email_directory = {
                'email': userTmp.email,
                'domain': request.META['HTTP_HOST'],
                'site_name': 'NoobNews',
                'uid': urlsafe_base64_encode(force_bytes(userTmp.pk)),
                'user': userTmp,
                'token': default_token_generator.make_token(userTmp),
                'protocol': 'http',
            }
            # Subject text from django authentication framework
            subject_template_name = 'registration/password_reset_subject.txt'
            # Template with the email body for reset the password
            email_template_name = 'registration/password_reset_email.html'
            # Function to load the subject template and set the required variables
            subject = loader.render_to_string(
                subject_template_name, blend_email_directory)
            subject = ''.join(subject.splitlines())
            # Function to load the body message template and set the required variables
            email = loader.render_to_string(
                email_template_name, blend_email_directory)
            # Function to send the email
            send_mail(subject, email, 'noobnewsa1@gmail.com', [
                      userTmp.email], fail_silently=False)
            # Message to notify the user that the email was sent successfully
            messages.success(request, 'An email has been sent to ' + userTmp.email +
                             '. Please check its inbox to continue reseting password.')
            # Redirect to the login page
            return HttpResponseRedirect(reverse('login'))

    else:
        reset_form = PasswordResetRequestForm()

    return render(request,
                  'noobnews/password_reset_form.html',
                  {
                      'reset_form': reset_form
                  })


def reset_password_confirm(request, uidb64=None, token=None):
    if request.method == 'POST':
        reset_confirm_form = SetPasswordForm(data=request.POST)
        UserModel = get_user_model()
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            if reset_confirm_form.is_valid():
                new_password = reset_confirm_form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return HttpResponseRedirect(reverse('login'))
            else:
                messages.error(
                    request, 'Password has not been reset due to an error.')
        else:
            messages.error(
                request, 'The reset password link is no longer valid.')
    else:
        reset_confirm_form = SetPasswordForm()

    return render(request,
                  'noobnews/password_reset_confirm.html',
                  {
                      'reset_confirm_form': reset_confirm_form
                  })


def contact_us(request):
    if request.method == 'POST':
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            videogame = None
            try:
                if contact_form.cleaned_data["video_games_list"]:
                    videogame = VideoGame.objects.get(
                        id=contact_form.cleaned_data["video_games_list"].id)
            except VideoGame.DoesNotExist:
                videogame = None
            type_suggestion = contact_form.cleaned_data["type_suggestion"]
            if videogame or type_suggestion == '1':
                email = contact_form.cleaned_data["email"]
                blend_email_directory = {
                    'fullname': contact_form.cleaned_data["full_name"],
                    'email': email,
                    'domain': request.META['HTTP_HOST'],
                    'site_name': 'NoobNews',
                    'videogame': videogame,
                    'message': contact_form.cleaned_data["contact_message"],
                    'type_suggestion': type_suggestion,
                    'protocol': 'http',
                }
                email_template_name = 'noobnews/contact_us_email.html'
                subject = 'Message from user'
                subject = ''.join(subject.splitlines())
                email_body = loader.render_to_string(
                    email_template_name, blend_email_directory)
                my_path = os.path.abspath(os.path.dirname(__file__))
                logo_path = os.path.join(
                    my_path, "../static/images/NoobNewslogo.png")
                fp = open(logo_path, 'rb')
                msgLogo = MIMEImage(fp.read())
                fp.close()
                msgLogo.add_header('Content-ID', '<nooblogo>')
                msg = EmailMultiAlternatives(subject, 'Important message', 'noobnewsa1@gmail.com', [
                                             'noobnewsa1@gmail.com', email])
                msg.attach_alternative(email_body, "text/html")
                msg.attach(msgLogo)
                if videogame is not None and videogame.image is not None:
                    built_path = '..' + videogame.image.name
                    videogame_path = os.path.join(
                        my_path, built_path)
                    fp = open(videogame_path, 'rb')
                    msgVideoGame = MIMEImage(fp.read())
                    fp.close()
                    msgVideoGame.add_header('Content-ID', '<videogamelogo>')
                    msg.attach(msgVideoGame)

                msg.send()
                messages.success(
                    request, 'An email has been sent to the site administrator. Thank you for helping us improve our site.')
                return HttpResponseRedirect(reverse('home'))
    else:
        contact_form = ContactForm()

    return render(request,
                  'noobnews/contact_form.html',
                  {
                      'contact_form': contact_form
                  })


def save_profile(backend, user, response, *args, **kwargs):
    if backend.name == 'twitter':
        try:
            profileTmp = UserProfile.objects.get(
                player_tag=user.username)
        except UserProfile.DoesNotExist:
            profileTmp = None

        if profileTmp is None:
            profile = UserProfile(user=user, player_tag=user.username)
            profile.save()


@login_required
def user_logout(request):

    # Since we know the user is logged in, we can now just log them out.
    logout(request)
# Take the user back to the homepage.
    return HttpResponseRedirect(reverse('home'))
   #  return render(request, 'noobnews/profile.html', context)


@login_required
def profile(request):
    # My video games library
    game = None
    selected_game = request.POST.get('selected_game')
    library = VideoGameList.objects.filter(
            user=request.user.userprofile)
    # Make a library for new users
    if not library:
        library_obj = VideoGameList.objects.create(user=request.user.userprofile)
    else:
        library_obj = VideoGameList.objects.get(list_id=library.first().list_id)

    if selected_game is None:
        game_obj = VideoGame.objects.get(id=56)
    else:
        game_obj = VideoGame.objects.get(id=selected_game)

    library_obj.userLibrary.add(game_obj)
    game = library_obj.userLibrary.all()

    # user profile has been updated
    #Update my name
    if request.method == 'POST':
        user_form_update = UserUpdateForm(
            request.POST, instance=request.user.userprofile)
        profile_form_update = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)
        #update my profile picture
        if profile_form_update.is_valid() and user_form_update.is_valid():
            profile_form_update.save()
            user_form_update.save()
            messages.success(request, f'Your information  has been  updated! ')
            return redirect('profile')

    else:

        # profile page before updates
        user_form_update = UserUpdateForm(
            instance=request.user.userprofile)

        profile_form_update = ProfileUpdateForm(
            instance=request.user.userprofile)

    context = {
        'user_form_update': user_form_update,
        'profile_form_update': profile_form_update,
        'game': game,




    }
    return render(request, 'noobnews/profile.html', context)

# test library funtionality
def video_game_list_add(request):
    selected_game = request.POST.get('selected_game')
    if selected_game is None:

        game_obj = VideoGame.objects.get(id=56)

        library = VideoGameList.objects.filter(
            user_id=request.user.userprofile)
        library_obj = VideoGameList.objects.get(list_id=library)
        library_obj.userLibrary.add(game_obj)
        game = library_obj.userLibrary.all()
        context = {'game': game}
    else:
        game_obj = VideoGame.objects.get(id=selected_game)

        library = VideoGameList.objects.filter(
            user_id=request.user.userprofile)
        library_obj = VideoGameList.objects.get(list_id=library)
        library_obj.userLibrary.add(game_obj)
        game = library_obj.userLibrary.all()

        context = {'game': game}

    return render(request, 'noobnews/cart.html', context)


class GameDetailView(DetailView):
    queryset = VideoGameList.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(GameDetailView, self).get_context_data(*args, **kwargs)
        request = self.request
        library_obj = VideoGameList.new_or_get(self.request)
        context['game'] = library_obj
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        instance = VideoGameList.objects.get(slug=slug, active=True)
        return instance
