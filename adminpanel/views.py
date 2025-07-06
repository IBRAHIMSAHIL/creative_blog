from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models.functions import TruncMonth
from django.db.models import Count
from blog.models import BlogPost, Comment
from collections import Counter

User = get_user_model()


@login_required
def dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Access denied. Admins only.")
        return redirect('blog_list')  # Or return a 403

    total_users = User.objects.count()
    total_posts = BlogPost.objects.count()
    total_comments = Comment.objects.count()
    recent_users = User.objects.order_by('-date_joined')[:5]
    recent_posts = BlogPost.objects.order_by('-created_at')[:5]

    # ✅ Monthly blog post count (convert to JSON-serializable list of dicts)
    monthly_posts_qs = (
        BlogPost.objects
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    monthly_posts = list(monthly_posts_qs)

    # ✅ Format month as "Jul 2025"
    for item in monthly_posts:
        item['month'] = item['month'].strftime('%b %Y')

    # ✅ Top 5 tags
    all_tags = []
    for blog in BlogPost.objects.all():
        all_tags.extend(blog.get_tag_list())

    top_tags = Counter(all_tags).most_common(5)

    return render(request, 'adminpanel/dashboard.html', {
        'total_users': total_users,
        'total_posts': total_posts,
        'total_comments': total_comments,
        'recent_users': recent_users,
        'recent_posts': recent_posts,
        'monthly_posts': monthly_posts,  # Will be passed to json_script
        'top_tags': top_tags,
        'quote': "Data is the new oil. Use it wisely."
    })
