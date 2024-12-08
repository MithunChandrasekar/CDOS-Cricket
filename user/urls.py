"""
This is the urls.py file fo rthe application redirected fomproject cricketapp
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('', views.homepage, name=""),
    path('register', views.register, name='register'),
    path('my-login', views.my_login, name='my-login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('match/<int:match_id>/', views.match_detail, name='match_detail'),
    path('update-scoreboard/<int:match_id>/', views.update_scoreboard, name='update_scoreboard'),
    path('user-logout', views.user_logout, name="user-logout"),
    path('profile-management', views.profile_management, name="profile-management"),
    path('delete-account', views.delete_account, name="delete-account"),
    # password management
    # 1- Allow us to enyer our email in order to receive a password reset link
    path('reset_password',
    auth_views.PasswordResetView.as_view(template_name = "user/password-reset.html"),
    name = "reset_password" ),

    # 2 showing us a success message stating an email was sent to reset our password
    path('reset_password_sent',
    auth_views.PasswordResetDoneView.as_view(template_name = "user/password-reset-sent.html"),
    name="password_reset_done"),

    #3 send a link to our email to reset the password
    path('reset/<uidb64>/<token>/',
    auth_views.PasswordResetConfirmView.as_view(template_name = "user/password-reset-form.html"),
    name ="password_reset_confirm"),

    #4 success message that our password was changed

    path('password_reset_complete',
auth_views.PasswordResetCompleteView.as_view(template_name = "user/password-reset-complete.html"),
name = "password_reset_complete"),
]
