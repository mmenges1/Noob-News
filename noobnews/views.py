from django.shortcuts import render
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
from noobnews.models import VideoGame
from noobnews.forms import UserForm, UserProfileForm


def home(request):
    videoGameList = VideoGame.objects.order_by('name')
    context_dict = {'videogames': videoGameList}
    # Render the response and send it back!
    return render(request, 'noobnews/home.html', context_dict)


def show_videogame(request, videogame_name_slug):
    context_dict = {}
    try:
        videoGame = VideoGame.objects.get(slug=videogame_name_slug)
        context_dict['videoGame'] = videoGame
    except VideoGame.DoesNotExist:
        context_dict['videoGame'] = None

    return render(request, 'noobnews/videogame.html', context_dict)


def get_category_list(max_results=0, starts_with=''):
    cat_list = []
    if starts_with:
        cat_list = VideoGame.objects.filter(name__istartswith=starts_with)
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
            user = user_form.save(commit=False)
            user.set_password(user.password)

            profile = profile_form.save(commit=False)
            user.username = user.email
            user.save()
            profile.user = user

            if 'user_profile_image' in request.FILES:
                profile.user_profile_image = request.FILES['user_profile_image']

            profile.save()

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
    auth_logout(request)
    return redirect('/')
