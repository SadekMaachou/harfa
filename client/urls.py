from django.urls import path
from .views import login_user, artiste_signup, standard_signup, home,all_conversations,conversation,reset_password

urlpatterns = [
    path('login/', login_user, name="login"),
    path('signup/artiste/', artiste_signup, name='artiste_signup'),
    path('signup/standard/', standard_signup, name='standard_signup'),
    path('home/',home,name='home'),
    path('conversation/',all_conversations),
    path('conversation_detail/', conversation, name='conversation'),
    path('reset',reset_password,name="reset_password"),
]