from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm


def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('blog:post_list'))
        else:
            args['login_error'] = 'User not found'
            return render(request, 'loginsys/login.html', args)
    else:
        return render(request, 'loginsys/login.html', args)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('blog:post_list'))


def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        new_user_form = UserCreationForm(request.POST)
        if new_user_form.is_valid():
            new_user_form.save()
            new_user = auth.authenticate(username=new_user_form.cleaned_data['username'], password=new_user_form.cleaned_data['password2'])
            auth.login(request, new_user)
            return HttpResponseRedirect(reverse('blog:post_list'))
        else:
            args['form'] = new_user_form
    return render(request, 'loginsys/register.html', args)
