from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from .forms import ExtendedUserCreationForm, UserProfileForm
def index(request):
    #Get the logged in username
    username = request.user.username
    context = {'username': username}
    return render(request, 'example/index.html', context)

#Only login users should be able to see profile.html page - This is a decorator
@login_required
def profile(request):
    return render(request, 'example/profile.html')

def register(request):
    if request.method == 'POST':
        form = ExtendedUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            profile.save()

            #After saving the username, logged in user and redirect it to index page
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request,user)
            return redirect('index')
    else:
        form = ExtendedUserCreationForm()
        profile_form = UserProfileForm()

    context = {'form': form, 'profile_form':profile_form}
    return render(request, 'example/register.html', context)