from django.urls import path
from . import views



app_name='home'
urlpatterns = [
    path('',views.HomeView.as_view(),name='home'),
    path('post/<int:post_id>/<slug:post_slug>/',views.PostView.as_view(),name='detail'),
    path('post/delete/<int:post_id>/<slug:post_slug>/',views.DeletePostView.as_view(),name='delete'),
    path('post/update/<int:post_id>/',views.UpdatePostView.as_view(),name='update'),
    path('post/create/',views.CreatePostView.as_view(),name='create'),
    path('reply/<int:post_id>/<int:comment_id>/',views.ReplyPostView.as_view(),name = 'add_reply'),
    path('like/<int:post_id>/',views.LikePostView.as_view(),name = 'like_post'),
]