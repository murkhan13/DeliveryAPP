from django.urls import path, include, re_path
from .views import *
from knox import views as knox_views

app_name = 'accounts'


urlpatterns = [
    re_path(r'^validate_phone/', ValidatePhoneSendOTP.as_view()),
    re_path("^auth/$", ValidateOtpAndAuthenticate.as_view()),
    re_path(r'^set_name/', SetUserName.as_view()),
    re_path(r'^change_phone', ChangePhone.as_view()),
    re_path("^logout/$", LogoutView.as_view())
]

'''re_path(r'^validate_phone_auth/', AuthValidatePhoneSendOTP.as_view()),
    re_path("^validate_otp/$", ValidateOTP.as_view()),
    re_path("^register/$", Register.as_view()),
    re_path("^authenticate", Authenticate.as_view()),
    re_path("^login/$", LoginAPI.as_view()),
    re_path("^logout/$", knox_views.LogoutView.as_view())'''