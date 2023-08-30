from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.views import OAuth2LoginView, OAuth2CallbackView


class CustomGoogleOAuth2Adapter(GoogleOAuth2Adapter):
    def get_authorization_url(self, request):
        self.set_callback_url(request)
        scope = self.get_scope(request)
        state = self.get_state(request)
        params = self.get_authorization_params(request)
        params['access_type'] = 'offline'
        params['prompt'] = 'consent'
        authorization_url = self.get_provider().get_auth_params_url(request, scope, state, **params)
        return authorization_url