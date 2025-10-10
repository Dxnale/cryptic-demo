import hmac

from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class CustomUserCreationForm(UserCreationForm):
    register_password = forms.CharField(
        label="Secret password required for registration",
        widget=forms.PasswordInput(),
        help_text="Enter the secret given to you by the administrator",
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2", "register_password")

    def clean_register_password(self):
        register_password = self.cleaned_data.get("register_password")

        if not register_password:
            raise ValidationError("La contraseña de registro es requerida.")

        expected_password = getattr(settings, "REGISTER_PASSWORD", None)
        if expected_password is None:
            raise ValidationError(
                "La configuración de contraseña de registro no está disponible."
            )

        # Use HMAC for secure constant-time comparison
        if not hmac.compare_digest(register_password, expected_password):
            raise ValidationError("La contraseña de registro es incorrecta.")

        return register_password
