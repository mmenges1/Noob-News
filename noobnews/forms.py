from django import forms
from string import Template
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import PrependedText
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from noobnews.models import UserProfile, Review, VideoGame


class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Full name'}))
    # name_icon = forms.CharField()
    email = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Create password'}))

    repeat_password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'placeholder': 'Repeat password'}))

    class Meta:
        model = User
        fields = ('first_name', 'email', 'password')

    helper = FormHelper()
    helper.layout = Layout(
        # first_name,
        PrependedText(
            'first_name', '<i class="fa fa-user"></i>'),
        # email,
        PrependedText(
            'email', '<i class="fa fa-envelope"></i>'),
        # password,
        PrependedText(
            'password', '<i class="fa fa-lock"></i>'),
        # repeat_password,
        PrependedText(
            'repeat_password', '<i class="fa fa-lock"></i>'),
    )


class UserProfileForm(forms.ModelForm):
    player_tag = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Player tag'}))

    user_profile_image = forms.FileField(label='', required=False)

    class Meta:
        model = UserProfile
        fields = ('player_tag', 'user_profile_image')

    helper = FormHelper()
    helper.layout = Layout(
        # player_tag,
        PrependedText(
            'player_tag', '<i class="fa fa-gamepad"></i>'),
        # 'user_profile_image',
        PrependedText(
            'user_profile_image', '<i class="fa fa-image"></i>')
    )
    helper.form_tag = False


class ReviewForm(forms.ModelForm):
    comment_rating = forms.CharField(
        label='', widget=forms.TextInput(attrs={'placeholder': 'Rating'}))
    comments = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'comment'}))
    # user_id= forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'User_id'}))

    class Meta:
        model = Review
        fields = ('comment_rating', 'comments', )


class UserUpdateForm(forms.ModelForm):

    player_tag = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Player tag'}))

    class Meta:
        model = UserProfile
        fields = ('player_tag',)


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user_profile_image',)


class PasswordResetRequestForm(forms.Form):
    email_or_playertag = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Email or player tag'}))


class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label='',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'New password'}))
    new_password2 = forms.CharField(label='',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new  password'}))

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2


class ContactForm(forms.Form):
    video_games_choices = VideoGame.objects.all()
    full_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Full name'}))
    email = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Email'}))
    type_suggestion = forms.ChoiceField(label='',
                                        choices=[(0, 'Select the suggestion type'),
                                                 (1, 'Suggest games to add'), (2, 'Suggest changes to games')])
    video_games_list = forms.ChoiceField(label='',
                                         choices=[("-", "Select a game")] + [(video_game.id, video_game.name)
                                                                             for video_game in video_games_choices])
    contact_message = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': 'Message'}))

    helper = FormHelper()
    helper.layout = Layout(
        PrependedText(
            'full_name', '<i class="fa fa-user"></i>'),
        PrependedText(
            'email', '<i class="fa fa-envelope"></i>'),
        PrependedText(
            'contact_message', '<i class="fas fa-comments"></i>'),
    )
