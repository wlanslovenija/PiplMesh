# Account view
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth import login, authenticate
from forms import RegistrationForm

# this method checks if form data are valid, saves new user.
# New user is authenticated, logged in and redirected to home page
def registration_view(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username, password = form.save()
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            return redirect('home')
    data = {'form': form}
    return render_to_response("registration.html", data, context_instance=RequestContext(request))