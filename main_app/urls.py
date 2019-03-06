from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('profile/<int:id>', views.ProfileView.as_view()),
    path('auth', views.AuthView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('register', views.RegisterView.as_view()),
    path('add_post', views.AddPostView.as_view()),
    path('edit_post/<int:id>', views.EditPostView.as_view()),
]
