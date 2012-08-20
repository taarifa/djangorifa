from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from users.forms import UserEditProfileForm

@login_required
def view(request):
    if request.method == "POST":
        return finished(request)

    # Get the current user's profile
    profile = [p for p in request.user.get_profile()._meta.fields if not p.name in ['user', 'id']]
    return render(request, "users/view.html", {'profile': profile})

@login_required
def edit(request):
    profile = request.user.get_profile()

    if request.method == "POST":
        form = UserEditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users-view'))

    form = UserEditProfileForm(instance=profile)
    # Show the user the form for editing their profile
    return render(request, "users/edit.html", {'form': form})
