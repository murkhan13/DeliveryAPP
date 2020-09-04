# from django.contrib.auth.backends import ModelBackend
# from django.conf import settings
# from django.contrib.auth.models import User
# from django.contrib.auth.hashers import check_password


# class PasswordlessAuthBackend(ModelBackend):
#     """ Log in to Django without providing a password.
#     """
#     def authenticate(self, request,phone=None, password=None):
#         # login_valid = (settings.ADMIN_LOGIN == phone)
#         # pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
#         # if login_valid and pwd_valid:
#         #     try:
#         #         user = User.objects.get(phone=phone)
#         #     except User.DoesNotExist:
#         #         return None
#         try:
#             user = User.objects.get(phone=phone)
#             return user
#         except User.DoesNotExist:
#             return None

#         return None

#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None