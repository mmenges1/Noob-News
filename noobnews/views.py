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
from django.contrib.auth import logout
from django.template import loader
from django.contrib import messages
from datetime import datetime
from noobnews.models import VideoGame, Genre, Review, User, UserProfile
from noobnews.forms import UserForm, UserProfileForm, ReviewForm, PasswordResetRequestForm, SetPasswordForm, ContactForm
from datetime import date
from social_django.models import UserSocialAuth

from noobnews.forms import ProfileUpdateForm, UserUpdateForm


def home(request):
    top40List = VideoGame.objects.order_by('-rating')[:40]
    newList = VideoGame.objects.order_by('-release')[:10]
    context_dict = {
        'newList': newList,
        'top40List': top40List,
        'user': request.user
    }
    # Render the response and send it back!
    return render(request, 'noobnews/home.html', context_dict)


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
                return HttpResponseRedirect(reverse('profile'))
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


def reset_password(request):
    if request.method == 'POST':
        reset_form = PasswordResetRequestForm(data=request.POST)
        if reset_form.is_valid():
            userTmp = None
            profileTmp = None
            data = reset_form.cleaned_data["email_or_playertag"]
            try:
                validate_email(data)
                is_email = True
            except ValidationError:
                is_email = False

            if is_email is True:
                try:
                    userTmp = User.objects.get(email=data)
                except User.DoesNotExist:
                    userTmp = None
            else:
                try:
                    profileTmp = UserProfile.objects.get(player_tag=data)
                except UserProfile.DoesNotExist:
                    profileTmp = None

            if userTmp is None and profileTmp is None:
                messages.error(
                    request, 'Sorry, we do not have any user associated with the information provided')
                return render(request,
                              'noobnews/password_reset_form.html',
                              {
                                  'reset_form': reset_form
                              })
            if profileTmp:
                userTmp = profileTmp.user

            blend_email_directory = {
                'email': userTmp.email,
                'domain': request.META['HTTP_HOST'],
                'site_name': 'NoobNews',
                'uid': urlsafe_base64_encode(force_bytes(userTmp.pk)),
                'user': userTmp,
                'token': default_token_generator.make_token(userTmp),
                'protocol': 'http',
            }
            subject_template_name = 'registration/password_reset_subject.txt'
            email_template_name = 'registration/password_reset_email.html'
            subject = loader.render_to_string(
                subject_template_name, blend_email_directory)
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(
                email_template_name, blend_email_directory)
            send_mail(subject, email, 'noobnewsa1@gmail.com', [
                      userTmp.email], fail_silently=False)
            messages.success(request, 'An email has been sent to ' + userTmp.email +
                             '. Please check its inbox to continue reseting password.')
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
    if request.method == 'POST':
        user_form_update = UserUpdateForm(
            request.POST, instance=request.user.userprofile)
        profile_form_update = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.userprofile)

        if profile_form_update.is_valid() and user_form_update.is_valid():
            profile_form_update.save()
            user_form_update.save()
            messages.success(request, f'Your information  has been  updated! ')
            return redirect('profile')

    else:
        user_form_update = UserUpdateForm(
            instance=request.user.userprofile)
        profile_form_update = ProfileUpdateForm(
            instance=request.user.userprofile)

    context = {
        'user_form_update': user_form_update,
        'profile_form_update': profile_form_update
    }

    return render(request, 'noobnews/profile.html', context)


# @login_required
# def update_profile(request):
 #   if request.method == 'POST':
    # user_form_update = UserUpdateForm(data=request.POST)
    # profile_form_update = ProfileUpdateForm(data=request.POST)

    # if profile_form_update.is_valid() and user_form_update.is_valid():
    # profile_form_update.save()
    # user_form_update.save()
    # messages.success(request, f'Your information  has been  updated! ')
    # return redirect('profile')

   # else:
    # messages.success(request, f'There is a form! ')
    # profile_form_update = ProfileUpdateForm()
    # user_form_update = UserUpdateForm()
    # context_a = {'profile_form_update': profile_form_update}
    # context = {'user_form_update ': user_form_update}

    # return render(request, 'noobnews/profile.html', {'user_form_update': user_form_update, 'profile_form_update': profile_form_update})
