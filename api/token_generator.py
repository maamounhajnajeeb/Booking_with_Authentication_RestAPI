from rest_framework_simplejwt.tokens import RefreshToken

from datetime import timedelta

class Token:
    def __init__(self, user) -> None:
        self.user = user
        
    def generate_token(self):
        token = RefreshToken.for_user(self.user).access_token
        token.set_exp(lifetime=timedelta(minutes=60))
        
        return token
    