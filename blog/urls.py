from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('post/<int:pk>/', views.blog_detail, name='blog_detail'),
    path('post/new/', views.blog_create, name='blog_create'),
    path('post/<int:pk>/edit/', views.blog_update, name='blog_update'),
    path('post/<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    path('comment/<int:comment_id>/edit/',
         views.comment_edit, name='comment_edit'),
    path('comment/<int:comment_id>/delete/',
         views.comment_delete, name='comment_delete'),
    path('admin-panel/', views.admin_dashboard, name='blog_admin_dashboard'),
    path('admin-panel/user/<int:user_id>/toggle/',
         views.toggle_user_status, name='toggle_user_status'),
    path('admin-panel/post/<int:post_id>/delete/',
         views.delete_post_admin, name='delete_post_admin'),
    path('admin-panel/comment/<int:comment_id>/delete/',
         views.delete_comment_admin, name='delete_comment_admin'),
    path('dashboard/', views.my_dashboard, name='user_dashboard'),
    path('tag/<str:tag>/', views.blogs_by_tag, name='blogs_by_tag'),
    path('post/<int:pk>/like/', views.toggle_like, name='toggle_like'),
    path('ajax/toggle-like/', views.ajax_toggle_like, name='ajax_toggle_like'),
    path('post/<int:pk>/bookmark/', views.toggle_bookmark, name='toggle_bookmark'),

]
