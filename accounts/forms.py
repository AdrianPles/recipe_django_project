from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator

User = get_user_model()

username_validator = RegexValidator(
    regex=r'^[\w\s.@+-]+$',
    message="Numele de utilizator poate conține litere (inclusiv diacritice), cifre, spații și caracterele @/./+/-/_."
)


class RegisterForm(UserCreationForm):
    # 2. Suprascriem câmpul username pentru a aplica validatorul nostru
    username = forms.CharField(
        validators=[username_validator],
        label="Nume utilizator",
        max_length=150,
        help_text="Litere (inclusiv diacritice), cifre, spații și caracterele @/./+/-/_."
    )
    class Meta:
        model = User                                 # now points to CustomUser
        fields = ("username", "email", "password1", "password2")