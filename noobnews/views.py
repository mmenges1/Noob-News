from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
from noobnews.models import VideoGame, Genre, Review, User, UserProfile
from noobnews.forms import UserForm, UserProfileForm,ReviewForm

from social_django.models import UserSocialAuth


def home(request):
    videoGameList = VideoGame.objects.order_by('name')
    context_dict = {
        'videogames': videoGameList,
        'user':request.user
        }
    # Render the response and send it back!
    return render(request, 'noobnews/home.html', context_dict)


def show_videogame(request, videogame_name_slug):
    context_dict = {}
    try:
        videoGame = VideoGame.objects.get(slug=videogame_name_slug)
        genres = Review.objects.filter(videogame=videoGame)
        users = UserProfile.objects.order_by('player_tag')
        context_dict = {'users': users,
                        'genres': genres, 'videoGame': videoGame}
    except VideoGame.DoesNotExist:
        context_dict['videoGame'] = None
        context_dict['genres'] = None
        context_dict['users'] = None

    return render(request, 'noobnews/videogame.html', context_dict)
#
# def top40(request):
#     context_dict = {}
#     try:
#         videoGame = VideoGame.objects.order_by('name')
#         context_dict['videoGame'] = videoGame
#     except VideoGame.DoesNotExist:
#         context_dict['videoGame'] = None
#     return render(request, 'noobnews/top40.html', context_dict)


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


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('mail')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Your account is disabled")
        else:
            message = "Invalid login details"
            messages.error(request, message)
            return render(request, 'noobnews/login.html', {'message': message})

    else:
        return render(request, 'noobnews/login.html', {})


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            repeat_password = user_form.cleaned_data['repeat_password']
            if(user_form.cleaned_data['password'] != repeat_password):
                messages.error(request, 'The passwords do not match!')
                return render(request,
                              'noobnews/register.html',
                              {
                                  'user_form': user_form,
                                  'profile_form': profile_form,
                              })
            try:
                userTmp = User.objects.get(
                    email=user_form.cleaned_data['email'])
            except User.DoesNotExist:
                userTmp = None

            if userTmp:
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
                profileTmp = UserProfile.objects.get(
                    player_tag=profile_form.cleaned_data['player_tag'])
            except UserProfile.DoesNotExist:
                profileTmp = None

            if profileTmp:
                messages.error(request, 'A user with the player tag ' +
                               profileTmp.player_tag+' already exists')
                return render(request,
                              'noobnews/register.html',
                              {
                                  'user_form': user_form,
                                  'profile_form': profile_form,
                                  'registered': registered
                              })

            registered = True
            messages.success(request, 'Account created successfully!')
            return render(request,
                          'noobnews/login.html',
                          {})
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


def user_logout(request):
    logout(request)
    return redirect('/')

def add_review(request,videogame_name_slug,user_player_tag):

    try:
        videogame = VideoGame.objects.get(slug=videogame_name_slug)
        user_id = UserProfile.objects.get(player_tag=user_player_tag)
        print (user_id)
    except:
        user_id = None
        videogame = None
        videogame_name_slug = None

    form = ReviewForm()
    print("1 checkpoint")
    # A HTTP POST?
    if request.method == 'POST':
        print("ITS A POST")
        form = ReviewForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            if videogame:
                review = form.save(commit=False)
                review.videogame = videogame
                if user_id:
                    review.user_id = user_id
                    review.save()
            return show_videogame(request, videogame_name_slug)
        else:
            print("ERROR")
            # The supplied form contained errors - just print them to the terminal.
            print(form.errors)
    # Will handle the bad form (or form details), new form or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'noobnews/addReview.html', {'form': form, 'videogame':videogame})
