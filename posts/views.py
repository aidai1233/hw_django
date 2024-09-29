from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Post, Comment
from posts.forms import PostForm2, CommentForm, SearchForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q


def text_view(request):
    return HttpResponse("Привет")


def html_view(request):
    if request.method == "GET":
        return render(request, 'base.html')


@login_required(login_url='login')
def list_view(request):
    if request.method == "GET":
        form = SearchForm(request.GET)
        posts = Post.objects.all()
        search = request.GET.get('search')
        tag = request.GET.getlist('tag')
        ordering = request.GET.get('ordering')
        if search:
            posts = posts.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        if tag:
            posts = posts.filter(tags__id__in=tag)
        if ordering:
            posts = posts.order_by()

        page = request.GET.get('page', 1)
        page = int(page)
        limit = 3
        max_pages = posts.count()/limit

        if round(max_pages)< max_pages:
            max_pages = round(max_pages)+1
        else:
            max_pages = round(max_pages)

        start = (page - 1) * limit
        end = page * limit
        posts = posts[start:end]
        context = {'posts': posts, 'form': form, 'max_pages': range(1, max_pages + 1)}
        return render(request, 'posts/post_list.html', context=context)


@login_required(login_url='login')
def detail_view(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "GET":
        form = CommentForm()
        comments = post.comments.all()
        return render(
            request, 'posts/post_detail.html',
            context={'post': post, 'form': form, 'comments': comments}
        )
    if request.method == "POST":
        form = CommentForm(request.POST)
        if not form.is_valid():
            return render(
                request,
                'posts/post_detail.html',
                context={'post': post, 'form': form, }
            )
        text = form.cleaned_data.get('text')
        Comment.objects.create(text=text, post=post)
        return redirect(f'/posts/{post.id}/')


def post_create_view(request):
    if request.method == "GET":
        form = PostForm2()
        return render(request, 'posts/post_create.html', context={'form': form})
    if request.method == "POST":
        form = PostForm2(request.POST, request.FILES)
        if not form.is_valid():
            return render(request, 'posts/post_create.html', context={'form':form})
        form.save()
        return redirect("/posts/")


