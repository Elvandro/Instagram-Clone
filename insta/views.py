from django.http  import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from . models import Profile, Image, Comment
from . forms import ImageUploadForm, ProfileUpdateForm, CommentForm, CaptionUpdateForm
from friendship.models import Friend, Follow, Block
from django.contrib.auth.decorators import login_required
import datetime as dt


# Create your views here.
@login_required(login_url='/accounts/login/')
def index(request):
    date = dt.date.today()
    friends = Friend.objects.friends(request.user)

    current_user = request.user
    return render(request, 'index.html')


@login_required(login_url='/accounts/login/')
def profile(request, profile_name):
    user_id = request.user.pk
    user = User.objects.get(username = username)
    profile = Profile.objects.get(user=user)
    images = Image.objects.filter(user_id = user)
    image_count = Image.objects.filter(user_id = user)
    number_of_friends = Friend.objects.friends(request.user)

    title = 'My Profile'
    return render(request, 'profile.html', {"title":title, "user":user, "images":images, "image_count":image_count, "profile":profile, "friends":number_of_friends})


@login_required(login_url='/accounts/login/')
def update_profile(request):
    current_user = request.user
    try:
        requested_profile = Profile.objects.get(user_id = current_user.id)
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST,request.FILES)

            if form.is_valid():
                requested_profile.profile_photo = form.cleaned_data['profile_photo']
                requested_profile.bio = form.cleaned_data['bio']
                requested_profile.profile_name = form.cleaned_data['profile_name']
                requested_profile.save_profile()
                return redirect(profile)
        else:
            form = ProfileUpdateForm()
    except:
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST,request.FILES)

            if form.is_valid():
                new_profile = Profile(profile_photo= form.cleaned_data['profile_photo'],bio = form.cleaned_data['bio'],profile_name = form.cleaned_data['profile_name'],user = current_user)
                new_profile.save_profile()
                return redirect(profile)
        else:
            form = ProfileUpdateForm()


    title = 'Update Profile'
    return render(request,'update_profile.html',{"title":title,"current_user":current_user,"form":form})



@login_required(login_url='/accounts/login/')
def post(request, profile_name):
    user = User.objects.get(profile_name = profile_name)
    current_user = request.user
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, files=request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = current_user
            image.save()

        return redirect(profile, current_user.profile_name)
    else:
        form = ImageUploadForm()

    return render(request, 'post.html', {"form":form})


@login_required(login_url='/accounts/login/')
def comment(request, image_id):
    comments = Comment.objects.filter(image_id=image_id)
    current_image = Image.objects.get(image_id=image_id)
    current_user = request.user
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit = False)
            comment.user_id= current_user
            comment.image_id = current_image
            comment.save()

            return redirect(index)
    else:
        comment_form = CommentForm()

    return render(request, 'comment.html', {"form":comment_form,"comments":comments})
