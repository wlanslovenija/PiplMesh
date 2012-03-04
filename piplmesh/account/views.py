# Account view
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.contrib.auth import login, authenticate
from forms import RegistrationForm

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