from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()

class RegisterForm(UserCreationForm):
    class Meta:
        model = User                                 # now points to CustomUser
        fields = ("username", "email", "password1", "password2")