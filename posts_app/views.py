from django.shortcuts import render, redirect
from main.models import Post, Comment, Like
from profile_app.models import Profile
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse


# Create your views here.
@login_required
def all_posts(request):
    posts = Post.objects.all()
    num_comments = [len(post.post_comments.all()) for post in posts]
    num_likes = [len(post.post_likes.all()) for post in posts]
    profile = Profile.objects.get(user=request.user)
    return render(request, 'posts_app/all_posts.html', {'posts': posts, 'profile': profile,
                                                        'num_comments': num_comments, 'num_likes': num_likes})


@login_required
def post_page(request, slug):
    post = Post.objects.get(slug=slug)
    comments = Comment.objects.filter(post_id=post.id)
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        body = request.POST.get('body')
        new_comment = Comment.objects.get_or_create(post = post, author = request.user, body=body)[0]
        new_comment.save()          
    return render(request, 'posts_app/post_page.html', {'post':post, 'post_id': post.id,
                                                        'comments': comments, 'profile': profile})


@login_required
def update_comment(request, comment_id, slug):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        body = request.POST.get('body')
        comment.body = body
        comment.save()
        return redirect('posts_app:page', slug=slug)
    else :
        return render(request, 'posts_app:page', slug=slug)
    
@login_required
def delete_comment(request, comment_id, slug):
    if request.method == 'POST':
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return redirect('posts_app:page', slug=slug)
    else :
        return render(request, 'posts_app:page', slug=slug)
       


@login_required
def my_posts(request):
    user = request.user
    posts = user.posts.all()
    num_comments = [len(post.post_comments.all()) for post in posts]
    num_likes = [len(post.post_likes.all()) for post in posts]

    profile = Profile.objects.get(user=request.user)
    return render(request, 'posts_app/my_posts.html', {'posts':posts, 'profile': profile, 
                                                       'num_comments': num_comments, 'num_likes':num_likes})

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    user = request.user
    posts = user.posts.all()
    profile = Profile.objects.get(user=request.user)
    return render(request, 'posts_app/my_posts.html', {'posts':posts, 'profile': profile })

@login_required
def new_post(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(post.title)
            post.save()
            return redirect('posts_app:my_posts')
    else:
        form = PostForm()

    return render(request, 'posts_app/new_post.html', {'form': form, 'profile': profile})


@login_required
def update_post(request, id):
    profile = Profile.objects.get(user=request.user)
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts_app:my_posts')
    else:
        form = PostForm(instance=post)
    return render(request, 'posts_app/update_post.html', {'form': form, 'profile': profile})

@login_required
def posts_commented(request):
    usr = request.user
    user_comments = usr.user_comments.all()
    posts_ids = list(dict.fromkeys([comment.post.id for comment in user_comments]))
    posts = [Post.objects.get(id=id) for id in posts_ids]
    num_comments = [len(post.post_comments.all()) for post in posts]
    num_likes = [len(post.post_likes.all()) for post in posts]
    profile = usr.profile
    return render(request, 'posts_app/posts_commented.html', {'posts': posts, 'profile': profile, 
                                                              'num_comments': num_comments, 'num_likes': num_likes})

@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        usr = request.user
        post = Post.objects.get(id=post_id)
        if len(post.post_likes.all().filter(user=usr).all())==0:
            like = Like(user = request.user, post = post)
            like.save()
            return redirect(reverse('posts_app:all_posts')+f'#post_{post_id}')
        else :
            return redirect(reverse('posts_app:all_posts')+f'#post_{post_id}')
        
@login_required
def like_post_commented(request, post_id):
    if request.method == 'POST':
        usr = request.user
        post = Post.objects.get(id=post_id)
        if len(post.post_likes.all().filter(user=usr).all())==0:
            like = Like(user = request.user, post = post)
            like.save()
            return redirect(reverse('posts_app:posts_commented')+f'#post_{post_id}')
        else :
            return redirect(reverse('posts_app:posts_commented')+f'#post_{post_id}')
