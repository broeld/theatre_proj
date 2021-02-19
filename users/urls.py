from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path("login/", views.LoginView.as_view(), name='login'),
    path("logout/", views.LogoutView.as_view(), name='logout'),
    path("signup/", views.UserRegistration.as_view(), name='signup'),

    path("password_change", views.PasswordChangeView.as_view(), name='password-change'),

    path("password_reset/", views.PasswordResetView.as_view(), name='password-reset'),
    path("password_reset_set/", views.PasswordResetSet.as_view(), name='password-reset-set'),
    path("password_reset_done/", views.PasswordResetDone.as_view(), name='password-reset-done'),

    path("profile/", views.UserPageView.as_view(), name='profile')
]