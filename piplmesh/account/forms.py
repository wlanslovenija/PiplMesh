from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.CharField(label=u"Username")
    first_name = forms.CharField(label=u"First name")
    last_name = forms.CharField(label=u"Last name")
    email = forms.EmailField(label=u"Email")
    password1 = forms.CharField(widget=forms.PasswordInput, label=u"Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label=u"Repeat password") 

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
        new_user.save() # save user in db
        return self.cleaned_data["username"], self.cleaned_data["password2"]
        