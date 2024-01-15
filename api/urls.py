from django.urls import path

from . import views 

app_name = "api"

urlpatterns = [
    # accounts & authentication
    path("user/", views.UserView.as_view(), name="user"),
    path("sign-up/", views.SignUpView.as_view(), name="sign-up"),
    path("log-in/", views.LogInView.as_view(), name="log-in"),
    path("log-out/", views.LogOutView.as_view(), name="log-out"),
    path("verify-email/", views.VerifyEmail.as_view(), name="verify-email"),
    path("reset-password/", views.ResetPass.as_view(), name="reset-password"),
    path("forget-password/", views.ForgetPass.as_view(), name="forget-password"),
    
    # booking
    path("booking/", views.BookingView.as_view(), name="booking"),
    path("book/<int:pk>/", views.SpecificBookingView.as_view(), name="specific-booking"),
]
