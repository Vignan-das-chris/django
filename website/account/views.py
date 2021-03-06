from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import LoginForm, UserRegistrationForm, DashboardForm
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])

            if user is not None and user.is_active:
                login(request, user)
                return HttpResponse('Authenticated sucesfully')

            else:
                return HttpResponse('Invalid login or disabled account')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    if request.method == "POST":
        form = DashboardForm(request.POST)

    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard'})


def register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():

            # create a new user object but avoid saving yet
            new_user = user_form.save(commit=False)
            # set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])

            # save the user object

            new_user.save()
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})

        else:
            user_form = UserRegistrationForm()
        return render(request,
                      'account/register.html',
                      {'user_form': user_form})
