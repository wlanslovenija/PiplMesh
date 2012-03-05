from datetime import datetime
from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import models as auth_models
from django.forms.extras import widgets
from django.utils.safestring import mark_safe
from models import UserProfile

class CaseInsensitveRegForm(auth_forms.UserCreationForm):
    """
    Class is used for registration with case-insensitive but case-preserving username. 
    To enable it simply extend registration form class with this class.
    """
    def clean_username(self):
	    username = super(CaseInsensitveRegForm, self).clean_username()
	    try:
		    auth_models.User.objects.get(username__iexact=username)
	    except auth_models.User.DoesNotExist:
	        return username
	    raise forms.ValidationError(u"A user with that username already exists.")
		
class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    """
    Renders horizontal radio buttons.
    Found here:
    https://wikis.utexas.edu/display/~bm6432/Django-Modifying+RadioSelect+Widget+to+have+horizontal+buttons
    """

    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class RegistrationForm(CaseInsensitveRegForm):
    """
	Class with user registration form
	"""
	
	#required data
    username = forms.CharField(label=u"Username *")
    email = forms.EmailField(label=u"Email *")
    password1 = forms.CharField(widget=forms.PasswordInput, label=u"Password *")
    password2 = forms.CharField(widget=forms.PasswordInput, label=u"Repeat password *") 
    first_name = forms.CharField(label=u"First name *")
    last_name = forms.CharField(label=u"Last name *")
	
	#additional information
    gender = forms.ChoiceField(label=u"Gender", required=False, choices=(('m','Male'),('f','Female')),widget=forms.RadioSelect(renderer=HorizontalRadioRenderer))   
    current_date = datetime.now()
    birthdate = forms.DateField(label=u"Birth date", required=False, widget=widgets.SelectDateWidget(years=[y for y in range(current_date.year,1900,-1)]))


    
    def clean_password2(self):
	    # This method checks whether the passwords match.
        if self.cleaned_data["password1"]==self.cleaned_data["password2"]:
            return self.cleaned_data["password2"]
        raise forms.ValidationError(u"Passwords do not match.")
    
    
    def clean_username(self):
	    # This method checks if username already exists.
	    username = super(RegistrationForm, self).clean_username()
	    try:
		    auth_models.User.objects.get(username__iexact=username)
	    except auth_models.User.DoesNotExist:
	        return username
	    raise forms.ValidationError(u"A user with that username already exists.")
    
   
    def save(self):	
	    # We first have to save user to db
        new_user = auth_models.User()
        new_user.username = self.cleaned_data["username"] # username
        new_user.first_name = self.cleaned_data["first_name"] # first name
        new_user.last_name = self.cleaned_data["last_name"] # last name
        new_user.email = self.cleaned_data["email"] # email
        new_user.set_password(self.cleaned_data["password2"]) # password
        new_user.save() # save user in db

        # Then we asign profile to this user
        profile = UserProfile()
        profile.user = new_user
        profile.gender = self.cleaned_data["gender"]
        profile.birthdate = self.cleaned_data["birthdate"]
        profile.save() # save profile

        return self.cleaned_data["username"], self.cleaned_data["password2"]