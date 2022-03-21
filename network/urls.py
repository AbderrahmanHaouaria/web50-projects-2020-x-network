from unicodedata import name
from django.urls import path
from . import views

app_name = "network"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:page_number>", views.index,),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following", views.following_page, name="following"),
    path("following/<int:page_number>", views.following_page, name="following"),
    path("profile/<str:username>", views.profile_page, name="profile"),
    path("profile/<str:username>/<int:page_number>", views.profile_page, name="profile"),
    path("update-post/<int:id>/<str:content>", views.update_post, name="update-post"),
    path("update-like/<int:id>/<str:value>", views.update_like, name="update-like"),
]
