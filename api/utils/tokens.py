from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    """Generate a dictionary containing access and refresh tokens"""

    refresh = RefreshToken.for_user(user)
    access = refresh.access_token
    tokens = {"access": str(access), "refresh": str(refresh)}

    return tokens
