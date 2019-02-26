from django import forms
from string import Template
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from crispy_forms.bootstrap import PrependedText
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from noobnews.models import UserProfile, Review
from datetime import date

class UserForm(forms.ModelForm):
    first_name = forms.CharField(label='', widget=forms.TextInput(
        attrs={'placeholder': 'Full name'}))
    #name_icon = forms.CharField()
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
    #
    # def _init_(self, *args, **kwargs):
    #     self._user = kwargs.pop('user')
    #     super(ReviewForm, self)._init_(*args, **kwargs)
    #
    # def save(self, commit=True):
    #     inst = super(ReviewForm, self).save(commit=False)
    #     inst.user_id = self._user
    #     if commit:
    #         inst.save()
    #         self.save_m2m()
    #     return inst

    comments = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'comment'}))
    comment_rating = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Rating'}))
    #user_id= forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'User_id'}))


    class Meta:
        model = Review
        fields = ('comments','comment_rating',)
