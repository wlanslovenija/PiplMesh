from django import forms as django_forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth import models as auth_models
from django.contrib.auth.models import User as auth_user
from django.utils.safestring import mark_safe as string_mark_safe
from django.forms.extras.widgets import SelectDateWidget as forms_date_widget
from datetime import datetime as date_time

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
	    raise django_forms.ValidationError(u"A user with that username already exists.")
		
class HorizontalRadioRenderer(django_forms.RadioSelect.renderer):
    """
    Renders horizontal radio buttons.
    Found here:
    https://wikis.utexas.edu/display/~bm6432/Django-Modifying+RadioSelect+Widget+to+have+horizontal+buttons
    """

    def render(self):
        return string_mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class RegistrationForm(CaseInsensitveRegForm):
    """
	Class with user registration form
	"""
	
	# Required data
    username = django_forms.CharField(label=u"Username")
    email = django_forms.EmailField(label=u"Email")
    password1 = django_forms.CharField(widget=django_forms.PasswordInput, label=u"Password")
    password2 = django_forms.CharField(widget=django_forms.PasswordInput, label=u"Repeat password") 
	
	# Additional information
    first_name = django_forms.CharField(label=u"First name",required=False)
    last_name = django_forms.CharField(label=u"Last name",required=False)
	
    gender = django_forms.ChoiceField(label=u"Gender",
	                           choices=((True,'Male'),(False,'Female')),
							   widget=django_forms.RadioSelect(renderer=HorizontalRadioRenderer),
							   required=False)
    
    current_date = date_time.now()
    birthdate = django_forms.DateField(label=u"Birth date",
	                            widget=forms_date_widget(years=[y for y in range(current_date.year,1900,-1)]),
								required=False)

    
    def clean_password2(self):
	    # This method checks whether the passwords match.
        if self.cleaned_data["password1"]==self.cleaned_data["password2"]:
            return self.cleaned_data["password2"]
        raise django_forms.ValidationError(u"Passwords do not match.")
    
    
    def clean_username(self):
	    # This method checks if username already exists.
	    username = super(RegistrationForm, self).clean_username()
	    try:
		    auth_models.User.objects.get(username__iexact=username)
	    except auth_models.User.DoesNotExist:
	        return username
	    raise django_forms.ValidationError(u"A user with that username already exists.")
    
   
    def save(self):
	    # This method saves new user data and returns username and password for authentication.
        new_user = User()
        new_user.username = self.cleaned_data["username"] # username
        new_user.first_name = self.cleaned_data["first_name"] # first name
        new_user.last_name = self.cleaned_data["last_name"] # last name
        new_user.email = self.cleaned_data["email"] # email
        new_user.set_password(self.cleaned_data["password2"]) # password
        new_user.gender = self.cleaned_data["gender"]
        new_user.birthdate = self.cleaned_data["birthdate"]
        new_user.save() # save user in db
        return self.cleaned_data["username"], self.cleaned_data["password2"]
        
