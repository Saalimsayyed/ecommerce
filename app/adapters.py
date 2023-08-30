from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        if sociallogin.account.provider == 'google':
            google_data = sociallogin.account.extra_data
            if 'email' in google_data:
                user.email = google_data['email']
                user.save()
        return user
