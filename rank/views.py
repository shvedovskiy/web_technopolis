from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import csrf

from .models import Category, Page
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    args = {'categories': category_list, 'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], '%Y-%m-%d %H:%M:%S')
        if (datetime.now() - last_visit_time).days > 0:
            visits += 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    args['visits'] = visits
    response = render(request, 'rank/index.html', args)
    return response


def about(request):
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0

    return render(request, 'rank/about.html', {'visits': count})


def category(request, category_name_slug):
    args = {}
    try:
        category_item = Category.objects.get(slug=category_name_slug)
        args['category_name'] = category_item.name
        args['category_name_slug'] = category_item.slug
        pages = Page.objects.filter(category=category_item)
        args['pages'] = pages
        args['category'] = category_item
    except Category.DoesNotExist:
        pass

    return render(request, 'rank/category.html', args)


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('rank:index'))
        else:
            print(form.errors)
    else:
        form = CategoryForm()
    return render(request, 'rank/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    category_item = get_object_or_404(Category, slug=category_name_slug)
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category_item:
                page = form.save(commit=False)
                page.category = category_item
                page.views = 0
                page.save()
                return HttpResponseRedirect(reverse('rank:category', args=(category_name_slug,)))
        else:
            print(form.errors)
    else:
        form = PageForm()

    args = {'form': form, 'category': category_item}
    return render(request, 'rank/add_page.html', args)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()
    return render(request, 'rank/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('rank:index'))
        else:
            args['login_error'] = 'User not found'
            return render(request, 'rank/login.html', args)
    else:
        return render(request, 'rank/login.html', args)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('rank:index'))
