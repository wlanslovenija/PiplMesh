from datetime import datetime

from django import forms
from django.conf import settings
from django.contrib.auth import forms as auth_forms, models as auth_models
from django.forms.extras import widgets
from django.utils import safestring
from django.utils.translation import ugettext_lazy as _

from account import models

# Form settings
GENDER_CHOICES = (
    ('male', _('Male')),
    ('female', _('Female'))
)

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    """
    Renders horizontal radio buttons.
    Found `here 
    <https://wikis.utexas.edu/display/~bm6432/Django-Modifying+RadioSelect+Widget+to+have+horizontal+buttons>`_.
    """

    def render(self):
        return safestring.mark_safe(u'\n'.join([u'%s\n' % widget for widget in self]))

class RegistrationForm(auth_forms.UserCreationForm):
    """
    Class with user registration form.
    """

    # Required data
    username = forms.CharField(label=_("Username *"))
    email = forms.EmailField(label=_("Email *"))
    password1 = forms.CharField(widget=forms.PasswordInput, label=_("Password *"))
    password2 = forms.CharField(widget=forms.PasswordInput, label=_("Repeat password *"))
    first_name = forms.CharField(label=_("First name *"))
    last_name = forms.CharField(label=_("Last name *"))
    
    # Additional information
    gender = forms.ChoiceField(label=_("Gender"), required=False, choices=(GENDER_CHOICES), widget=forms.RadioSelect(renderer=HorizontalRadioRenderer))    
    current_date = datetime.now()
    birthdate = forms.DateField(label=_("Birth date"), required=False, widget=widgets.SelectDateWidget(years=[y for y in range(current_date.year, 1900, -1)]))
    
    def clean_password2(self):
        # This method checks whether the passwords match
        if self.cleaned_data['password1'] == self.cleaned_data['password2']:
            return self.cleaned_data['password2']
        raise forms.ValidationError(_("Passwords do not match."))
       
    def clean_username(self):
        # This method checks whether the username exists in case-insensitive manner
        username = super(RegistrationForm, self).clean_username()
        try:
            auth_models.User.objects.get(username__iexact=username)
        except auth_models.User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))
      
    def save(self):	
        # We first have to save user to database
        new_user = auth_models.User(username=self.cleaned_data['username'],
                                    first_name=self.cleaned_data['first_name'],
                                    last_name=self.cleaned_data['last_name'],
                                    email=self.cleaned_data['email'])			
                                    
        new_user.set_password(self.cleaned_data['password2'])
        new_user.save()
        
        # Then we asign profile to this user
        profile = models.UserProfile(user=new_user,gender=self.cleaned_data['gender'],birthdate=self.cleaned_data['birthdate'])
        profile.save()

        return self.cleaned_data['username'], self.cleaned_data['password2']