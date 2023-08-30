from django.contrib.auth import get_user_model
from allauth.account.auth_backends import AuthenticationBackend

class EmailAuthenticationBackend(AuthenticationBackend):
    def authenticate(self, request, **credentials):
        UserModel = get_user_model()
        try:
            print(f"{credentials=}")
            user = UserModel.objects.get(email=credentials['username'])
        except KeyError:
            user = UserModel.objects.get(email=credentials['email'])
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(credentials['password']):
                return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
