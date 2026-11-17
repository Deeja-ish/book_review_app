from django.urls import path
from .views import RegistrationView, ForgotPasswordView, ResetPasswordView, VerifyOTPView, ChangePasswordView, LoginView, ProfileView, AllUserView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register_view"),
    path("login/", LoginView.as_view(), name="login_view"),
    path("verify_otp/", VerifyOTPView.as_view(), name='verify_otp'),
    path("change_password/", ChangePasswordView.as_view(), name='change_password'),
    path("forgot_password/", ForgotPasswordView.as_view(), name='forgot_password'),
    path("reset_password/", ResetPasswordView.as_view(), name='reset_password'),
    path("profile/", ProfileView.as_view(), name='profile_view'),
    path("all_users/", AllUserView.as_view(), name='all_users')
]