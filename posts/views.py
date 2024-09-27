from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Post, Comment
from posts.forms import PostForm2, CommentForm
from django.shortcuts import render, redirect


def text_view(request):
    return HttpResponse("Привет")


def html_view(request):
    if request.method == "GET":
        return render(request, 'base.html')


def list_view(request):
    if request.method == "GET":
        posts = Post.objects.all()
        return render(request, 'posts/post_list.html', context={'posts': posts})


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


