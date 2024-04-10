from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follow, Like
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Post


def index(request):
    posts_list = Post.objects.all().order_by('-timestamp')
    # Add the is_liked attribute to each post
    # Add the is_liked attribute to each post
    for post in posts_list:
        post.is_liked = post.post_like.filter(user=request.user).exists() if request.user.is_authenticated else False
    paginator = Paginator(posts_list, 10)  

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'network/index.html', {
        'page_obj': page_obj,
        'posts': posts_list,
       
    })

def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    allPosts = Post.objects.filter(user=user).order_by("id").reverse()

    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(follower=user)

    try:
        status = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(status) != 0:
            isFollowing = True
        else:
            isFollowing = False
    except:
        isFollowing = False


    paginator = Paginator(allPosts, 10)
    page_number = request.GET.get('page')
    posts_of_the_page = paginator.get_page(page_number)
    return render(request, 'network/profile.html', {
        "username": user.username,
        'page_obj': posts_of_the_page,
        "following": following,
        "followers": followers,
        "isFollowing": isFollowing,
        "user_profile": user
        })

def follow(request):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userfollow)
    fl = Follow(user=currentUser, follower=userfollowData)
    fl.save()
    user_id = userfollowData.id 
    return HttpResponseRedirect(reverse('profile', args=[user_id]))


def unfollow(request):
    userfollow = request.POST['userfollow']
    currentUser = User.objects.get(pk=request.user.id)
    userfollowData = User.objects.get(username=userfollow)
    uf = Follow.objects.get(user=currentUser, follower=userfollowData)
    uf.delete()
    user_id = userfollowData.id 
    return HttpResponseRedirect(reverse('profile', kwargs={'user_id': user_id}))


@login_required
def following(request):
    # This fetches IDs of users that the current user follows
    followed_users_ids = Follow.objects.filter(user=request.user).values_list('follower_id', flat=True)
    # Fetch posts created by these followed users
    posts = Post.objects.filter(user_id__in=followed_users_ids).order_by('-timestamp')
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'network/following.html', {'page_obj': page_obj})


def new_post(request):
    if request.method == "POST":
        content = request.POST["content"]
        user = User.objects.get(pk=request.user.id )
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/new_post.html")
    

def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        edit_post = Post.objects.get(pk=post_id)
        edit_post.content = data["content"]
        edit_post.save()
        return JsonResponse({"message": "Change successful", "data": data["content"]})



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")




@login_required
@csrf_exempt
def like_post(request, post_id):
    try:
        post = get_object_or_404(Post, pk=post_id)
        if Like.objects.filter(post=post, user=request.user).exists():
            Like.objects.filter(post=post, user=request.user).delete()
            is_liked = False
        else:
            Like.objects.create(post=post, user=request.user)
            is_liked = True
        likes = post.post_like.count()
        return JsonResponse({'likes': likes, 'is_liked': is_liked})
    except Exception as e:
        print(f"An error occurred: {e}")
        return JsonResponse({'error': str(e)}, status=500)