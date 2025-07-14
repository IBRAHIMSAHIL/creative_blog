from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import CommentForm
from users.models import CustomUser
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Comment, BlogPost, Like


def blog_list(request):
    query = request.GET.get('q', '')
    tag_filter = request.GET.get('tag', '')

    blogs = BlogPost.objects.all()

    if query:
        blogs = blogs.filter(Q(title__icontains=query) |
                             Q(author__username__icontains=query))

    if tag_filter:
        blogs = blogs.filter(tags__icontains=tag_filter)

    # Collect all unique tags
    all_tags = set()
    for blog in BlogPost.objects.all():
        all_tags.update(blog.get_tag_list())

    paginator = Paginator(blogs.order_by('-created_at'), 6)
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)

    return render(request, 'blog/blog_list.html', {
        'blogs': blogs,
        'query': query,
        'tag_filter': tag_filter,  # ✅ MUST BE INCLUDED
        'all_tags': sorted(all_tags)
    })

# Create Blog


@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'Your blog has been posted!')
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = BlogPostForm()
    return render(request, 'blog/blog_form.html', {'form': form})

# Update Blog


@login_required
def blog_update(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog updated successfully!')
            return redirect('blog_detail', pk=blog.pk)
    else:
        form = BlogPostForm(instance=blog)
    return render(request, 'blog/blog_form.html', {'form': form})

# Delete Blog


@login_required
def blog_delete(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk, author=request.user)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog deleted.')
        return redirect('blog_list')
    return render(request, 'blog/blog_confirm_delete.html', {'blog': blog})


def blog_detail(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    comments = blog.comments.all().order_by('-created_at')

    # Count views (skip author)
    if request.user != blog.author:
        blog.views += 1
        blog.save(update_fields=['views'])

    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(blog=blog, user=request.user).exists()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.blog = blog
                comment.author = request.user
                comment.save()
                messages.success(request, "Comment added.")
                return redirect('blog_detail', pk=pk)
        else:
            messages.error(request, "You must be logged in to comment.")
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'blog/blog_detail.html', {
        'blog': blog,
        'comments': comments,
        'form': form,
        'is_liked': is_liked,
    })


@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            messages.success(request, "Comment updated.")
            return redirect('blog_detail', pk=comment.blog.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id, author=request.user)
    blog_id = comment.blog.pk
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted.")
        return redirect('blog_detail', pk=blog_id)
    return render(request, 'blog/comment_confirm_delete.html', {'comment': comment})


@staff_member_required
def admin_dashboard(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    posts = BlogPost.objects.all().order_by('-created_at')
    comments = Comment.objects.all().order_by('-created_at')

    return render(request, 'blog/admin_dashboard.html', {
        'users': users,
        'posts': posts,
        'comments': comments,
    })


User = get_user_model()


@staff_member_required
@require_POST
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if not user.is_superuser:  # Don't allow blocking superusers
        user.is_active = not user.is_active
        user.save()
        messages.success(
            request, f"User {'unblocked' if user.is_active else 'blocked'} successfully.")
    return redirect('blog_admin_dashboard')


@staff_member_required
@require_POST
def delete_post_admin(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect('blog_admin_dashboard')


@staff_member_required
@require_POST
def delete_comment_admin(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    messages.success(request, "Comment deleted successfully.")
    return redirect('blog_admin_dashboard')


@login_required
def my_dashboard(request):
    user_posts = BlogPost.objects.filter(
        author=request.user).order_by('-created_at')
    user_comments = Comment.objects.filter(
        author=request.user).order_by('-created_at')

    post_count = user_posts.count()
    comment_count = user_comments.count()

    latest_post = user_posts.first()
    latest_comment = user_comments.first()

    return render(request, 'blog/user_dashboard.html', {
        'user_posts': user_posts,
        'user_comments': user_comments,
        'post_count': post_count,
        'comment_count': comment_count,
        'latest_post': latest_post,
        'latest_comment': latest_comment,
    })


def blogs_by_tag(request, tag):
    blogs = BlogPost.objects.filter(
        tags__icontains=tag).order_by('-created_at')
    return render(request, 'blog/blog_list.html', {'blogs': blogs, 'query': tag})


@require_POST
@login_required
def toggle_like(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)
    like, created = Like.objects.get_or_create(user=request.user, blog=blog)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'totalLikes': blog.total_likes  # ✅ fixed here
    })


@require_POST
@login_required
def ajax_toggle_like(request):
    blog_id = request.POST.get('blog_id')
    blog = BlogPost.objects.get(pk=blog_id)

    like, created = Like.objects.get_or_create(blog=blog, user=request.user)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': blog.likes.count()
    })


@login_required
def toggle_bookmark(request, pk):
    blog = get_object_or_404(BlogPost, pk=pk)

    if blog in request.user.bookmarks.all():
        request.user.bookmarks.remove(blog)
        bookmarked = False
    else:
        request.user.bookmarks.add(blog)
        bookmarked = True

    return JsonResponse({
        'bookmarked': bookmarked
    })
