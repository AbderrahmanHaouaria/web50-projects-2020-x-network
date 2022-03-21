from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm, Textarea, HiddenInput
from .models import User, Post
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


def index(request, page_number=1):

    # Create new form by using the Post model
    class PostForm(ModelForm):
        class Meta:
            model = Post
            fields = ['content', 'user']
            labels = {
                'content': 'New Post'
            }
            widgets = {
                'content': Textarea(attrs={'class': 'form-control', 'rows': 2}),
                'user': HiddenInput
            }

    # Instantiate and save new post form
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")

    # Initialize the 'user' field with the current user
    else:
        form = PostForm(initial={"user": request.user})

    # Retrieve all posts and save them in a list, in reverse chronological order
    posts = Post.objects.all()
    posts = posts[::-1]

    p = Paginator(posts, 10)
    current_page = p.page(page_number)
    page_posts = current_page.object_list

    return render(request, "network/index.html", {
        "form": form,
        "posts": page_posts,
        "num_pages": p.num_pages,
        "current_page": current_page,
        "has_next": current_page.has_next(),
        "has_prev": current_page.has_previous(),
        "next_num": current_page.next_page_number,
        "prev_num": current_page.previous_page_number,
        "p": p
    })

@csrf_exempt
def profile_page(request, username, page_number=1):

    # Determine the user who owns this profile
    profile_owner = User.objects.get(username=username)

    # Check if user who's visiting this page is in the followers field of profile_owner
    if request.user in profile_owner.followers.all():
        isFollower = True
    else:
        isFollower = False

    # Implement the ability to Follow or Unfollow
    if request.method == "POST":
        if not isFollower:
            profile_owner.followers.add(request.user)
            request.user.following.add(profile_owner)
        else:
            profile_owner.followers.remove(request.user)
            request.user.following.remove(profile_owner)

    # Get current number of followers and following
    followers = profile_owner.followers.aggregate(Count("id"))
    following = profile_owner.following.aggregate(Count("id"))

    # Retrieve all user posts and save them in a list
    posts = profile_owner.posts.all()
    posts = posts[::-1]

    p = Paginator(posts, 10)
    current_page = p.page(page_number)
    page_posts = current_page.object_list

    return render(request, "network/profile.html", {
        "owner": str(profile_owner.username),
        "visitor": str(request.user),
        "followers": followers["id__count"],
        "following": following["id__count"],
        "posts": page_posts,
        "num_pages": p.num_pages,
        "current_page": current_page,
        "has_next": current_page.has_next(),
        "has_prev": current_page.has_previous(),
        "next_num": current_page.next_page_number,
        "prev_num": current_page.previous_page_number,
        "p": p,
        "isFollower": isFollower
    })


def following_page(request, page_number=1):

    visitor = request.user

    # Retrieve following users' posts and store them in a list
    posts = []
    for user in visitor.following.all():
        for post in user.posts.all():
            posts.append(post)

    p = Paginator(posts, 10)
    current_page = p.page(page_number)
    page_posts = current_page.object_list

    return render(request, "network/following.html", {
        "posts": page_posts,
        "num_pages": p.num_pages,
        "current_page": current_page,
        "has_next": current_page.has_next(),
        "has_prev": current_page.has_previous(),
        "next_num": current_page.next_page_number,
        "prev_num": current_page.previous_page_number,
        "p": p,
    })

@csrf_exempt
def update_post(request, id, content):
    if request.method == "POST":
        
        # Get the post that's edited, update and save it
        post = Post.objects.get(id=id)
        post.content = content
        post.save(update_fields=['content'])

    else:
        return HttpResponseRedirect("network:index")

@csrf_exempt
def update_like(request, id, value):
    if request.method == "POST":

        # Get the post that's liked/unliked, update and save it
        if value == "Unlike":
            Post.objects.get(id=id).likes.remove(request.user)
        else:
            Post.objects.get(id=id).likes.add(request.user)

    else:
        return HttpResponseRedirect("network:index")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("network:index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("network:index"))


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
        return HttpResponseRedirect(reverse("network:index"))
    else:
        return render(request, "network/register.html")
