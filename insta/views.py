from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.auth.models import User
from . models import Profile, Image, Comment
# from django.http  import Http404
from . forms import ImageUploadForm, ProfileUpdateForm, CommentForm, CaptionUpdateForm
from friendship.models import Friend, Follow, Block
import datetime as dt


# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    current_user = request.user
    images = Image.objects.all()
    profiles = Profile.objects.all()
    user = Profile.objects.filter(user=current_user)
    comments = Comment.objects.all()
    locals = {
        "current_user": current_user,
        "images": images,
        "profiles": profiles,
        "user": user,
        "comments":comments
    }
    return render(request, 'index.html', locals)

@login_required(login_url='/accounts/login/')
def post(request):
    current_user = request.user
    profiles = Profile.objects.all()
    form = ImageUploadForm()
    for profile in profiles:
        if profile.user.id == current_user.id:
            if request.method == 'POST':
                form = ImageUploadForm(request.POST, request.FILES)
                if form.is_valid():
                    post = form.save(commit=False)
                    post.user_key = current_user
                    post.profile_key = profile
                    post.save()
                    return redirect('index')
            else:
                form = ImageUploadForm()
    return render(request, 'post.html', {"post_form":form, "user": current_user})

@login_required(login_url='/accounts/login/')
def comment(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    current_user = request.user
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.image = image
            comment.creator = current_user
            comment.save()
            return redirect('index')
    else:
        form = CommentForm()

    content = {
        "comment_form": form,
    }
    return render(request, 'comment.html', content)

@login_required(login_url='/accounts/login/')
def search_result(request):
    if 'query' in request.GET and request.GET['query']:
        query = request.GET.get("query")
        user = Profile.find_profile(query)
        images = Image.objects.all()
        message = f"query"

        content = {
            "message": message,
            "found": user,
            "images": images,
        }

        return render(request, 'search.html', content)
    else:
        message = "You haven't searched for anyone"
        return render(request, 'search.html', {"message": message})


@login_required(login_url='/accounts/login/')
def like(request, operation, pk):
    image = image = get_object_or_404(Image, pk=pk)
    if operation == 'like':
        image.likes = image.likes + 1
        image.save()
    elif operation == 'unlike':
        image.likes = image.likes - 1
        image.save()
    return redirect('index')

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    images = Image.objects.filter(user_key=request.user)
    profiles = Profile.objects.filter(user=request.user)
    content = {
        "current_user": current_user,
        "images": images,
        "profiles": profiles
    }
    return render(request, 'profile.html', content)


@login_required(login_url='/accounts/login/')
def update_profile(request):
    current_user = request.user
    user_profile = Profile.objects.filter(user_id=current_user)
    form = ProfileUpdateForm()
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = current_user
            user_profile.save()
            return redirect('index')
    else:
        form = ProfileUpdateForm()

        content = {
            "form": form,
        }
        return render(request, 'updateprofile.html', content)
