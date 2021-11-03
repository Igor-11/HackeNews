from django.urls import path
from .views import *
 
urlpatterns = [
    path('',post_list_view, name='home'),
    path('new',new_post_list_view, name='new_home'),
    path('past',past_post_list_view, name='past_home'),
    path('user/<username>', user_info_view, name='user_info'),
    path('posts/<username>',user_submissions, name='user_posts'),
    path('post/<int:id>',comment_list_view, name='post'),
    path('submit',submit_post_view, name='submit'),
    path('signin',signin, name='signin'),
    path('signup',signup, name='signup'),
    path('signout',signout, name='signout'),
    path('vote/<int:id>',up_vote_view,name='vote'),
    path('downvote/<int:id>',down_vote_view,name='dvote'),
    path('edit/<int:id>',edit_list_view, name='edit'),
    path('post/<int:id1>/comment/<int:id2>',comment_reply_view,name='reply'),
]