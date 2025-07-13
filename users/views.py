from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .forms import ProfileUpdateForm


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Account created successfully! Please login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

    from blog.models import BlogPost, Comment

    user = request.user
    posts = BlogPost.objects.filter(author=user)
    comments = Comment.objects.filter(author=user)
    bookmarks = user.bookmarks.all() if hasattr(user, 'bookmarks') else []

    context = {
        'form': form,
        'posts': posts,
        'comments': comments,
        'bookmarks': bookmarks,
    }

    return render(request, 'users/profile.html', context)


@login_required
def my_bookmarks(request):
    bookmarks = request.user.bookmarks.all()
    return render(request, 'users/my_bookmarks.html', {'bookmarks': bookmarks})
