from django.contrib.auth.backends import BaseBackend, ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class CustomBackend(BaseBackend):
    def authenticate(self, request, correo_usu=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(correo_usu=correo_usu)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

class EmailBackend(ModelBackend):
    def authenticate(self, request, correo_usu=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(correo_usu=correo_usu)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
