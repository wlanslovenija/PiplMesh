from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.template import context

from account import forms

# This method checks if form data are valid, saves new user
# New user is authenticated, logged in and redirected to home page
def registration_view(request):
    # Redirect user to home page if logged in
    if request.user.is_authenticated():
        return redirect('home')
    form = forms.RegistrationForm()
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            username, password = form.save()
            new_user = auth.authenticate(username=username, password=password)
            auth.login(request, new_user)
            return redirect('home')
    data = {'form': form}
    return render_to_response("registration.html", data, context_instance=context.RequestContext(request))