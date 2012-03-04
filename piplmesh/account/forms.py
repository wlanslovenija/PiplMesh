from django import forms
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.forms.extras.widgets import SelectDateWidget
from models import UserProfile
import datetime


class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    """renders horizontal radio buttons.
    found here:
    https://wikis.utexas.edu/display/~bm6432/Django-Modifying+RadioSelect+Widget+to+have+horizontal+buttons
    """

    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class RegistrationForm(forms.Form):
	#required data
    username = forms.CharField(label=u"Username *")
    email = forms.EmailField(label=u"Email *")
    password1 = forms.CharField(widget=forms.PasswordInput, label=u"Password *")
    password2 = forms.CharField(widget=forms.PasswordInput, label=u"Repeat password *") 
	
	#additional information
    first_name = forms.CharField(label=u"First name *")
    last_name = forms.CharField(label=u"Last name *")
    gender = forms.ChoiceField(label=u"Gender", required=False, choices=(('m','Male'),('f','Female')),widget=forms.RadioSelect(renderer=HorizontalRadioRenderer))
    
    current_date = datetime.datetime.now()
    birthdate = forms.DateField(label=u"Birth date", required=False, widget=SelectDateWidget(years=[y for y in range(current_date.year,1900,-1)]))

    # This method checks whether the passwords match.
    def clean_password2(self):
        if self.cleaned_data["password1"]==self.cleaned_data["password2"]:
            return self.cleaned_data["password2"]
        raise forms.ValidationError(u"Passwords do not match.")
    
    # This method checks if username already exists.
    def clean_username(self):
        user_number = User.objects.filter(username=self.cleaned_data["username"]).count();
        if(user_number == 0):
            return self.cleaned_data["username"]
        raise forms.ValidationError(u"Username already exists.")
    
    # This method saves new user data and returns username and password for authentication.
    def save(self):
        new_user = User()
        new_user.username = self.cleaned_data["username"] # username
        new_user.first_name = self.cleaned_data["first_name"] # first name
        new_user.last_name = self.cleaned_data["last_name"] # last name
        new_user.email = self.cleaned_data["email"] # email
        new_user.set_password(self.cleaned_data["password2"]) # password
        
        # We first have to save user to db
        new_user.save() # save user in db
        
        # Then we asign profile to this user
        profile.user = new_user
        profile.gender = self.cleaned_data["gender"]
        profile.birthdate = self.cleaned_data["birthdate"]
        profile.save() # save profile

        return self.cleaned_data["username"], self.cleaned_data["password2"]
        