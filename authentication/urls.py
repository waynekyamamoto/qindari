from django.urls import path, include
from . import views

urlpatterns = [
    path('signup', views.signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),

    # User requests to change password
    path('password_change_request/', views.password_change_request, name='password_change_request'),
    # Email sent with password change link
    path('password_change_done/', views.password_change_done, name='password_change_request_done'),

    # Allow user to reset password after clicking through on email link
    path('password_reset_request/<uidb64>/<token>', views.password_reset_request, name='password_reset_request'),
    # Password reset completed
    #path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
]

