from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.template.context_processors import csrf
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post, Comment
from .forms import PostForm, CommentForm


def post_list(request, page_number=1):
    posts = Post.objects\
        .filter(published_date__lte=timezone.now())\
        .order_by('published_date')
    current_page = Paginator(posts, 5)
    return render(request, 'blog/post_list.html', {
        'posts': current_page.page(page_number),
        'username': auth.get_user(request).username
    })


def post_detail(request, pk):
    comment_form = CommentForm()
    args = {}
    args.update(csrf(request))
    args['post'] = get_object_or_404(Post, pk=pk)
    args['form'] = comment_form
    args['username'] = auth.get_user(request).username
    return render(request, 'blog/post_detail.html', args)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.POST and ('pause' not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            request.session.set_expiry(60)
            request.session['pause'] = True
    return HttpResponseRedirect(reverse('blog:post_detail', args=(pk,)))


@login_required
def post_new(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('blog:post_detail', args=(post.pk,)))
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('blog:post_detail', args=(post.pk,)))
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def add_like(request, pk, page=1):
    if pk in request.COOKIES:
        return HttpResponseRedirect(reverse('blog:page_post_list', args=(page,)))
    else:
        post = get_object_or_404(Post, pk=pk)
        post.likes += 1
        post.save()
        response = HttpResponseRedirect(reverse('blog:page_post_list', args=(page,)))
        response.set_cookie(pk, 'test')
        return response


@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return HttpResponseRedirect(reverse('blog:post_detail', args=(pk,)))


@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return HttpResponseRedirect(reverse('blog:post_list'))


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return HttpResponseRedirect(reverse('blog:post_detail', args=(comment.post.pk,)))


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return HttpResponseRedirect(reverse('blog:post_detail', args=(post_pk,)))
