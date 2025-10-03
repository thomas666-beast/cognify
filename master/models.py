from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ValidationError
import re


class Master(models.Model):
    # Use Django's default AutoField (no need to explicitly define 'id')
    username = models.CharField(
        unique=True,
        max_length=100,
        verbose_name="Username",
        help_text="Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only.",
        error_messages={
            'unique': "A user with that username already exists.",
        }
    )

    password = models.CharField(
        max_length=128,  # Standard length for hashed passwords
        verbose_name="Password",
        help_text="Use a strong password with at least 8 characters."
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Designates whether this user can log in."
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date joined"
    )

    last_login = models.DateTimeField(
        auto_now=True,
        verbose_name="Last login"
    )

    class Meta:
        verbose_name = "Master User"
        verbose_name_plural = "Master Users"
        ordering = ['username']
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['date_joined']),
        ]

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Hash password before saving if it's not already hashed
        if self.password and not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)

        # Validate username format
        self.full_clean()

        super().save(*args, **kwargs)

    def clean(self):
        """Custom validation"""
        super().clean()

        # Username validation
        if self.username:
            if not re.match(r'^[\w.@+-]+\Z', self.username):
                raise ValidationError({
                    'username': 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.'
                })
            if len(self.username) < 3:
                raise ValidationError({
                    'username': 'Username must be at least 3 characters long.'
                })

        # Password strength validation (only for new passwords)
        if self.password and len(self.password) < 8 and not self.password.startswith(
                ('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            raise ValidationError({
                'password': 'Password must be at least 8 characters long.'
            })

    def check_password(self, raw_password):
        """Check the password against the stored hash"""
        return check_password(raw_password, self.password)

    def set_password(self, raw_password):
        """Set a new password (hashed)"""
        self.password = make_password(raw_password)

    @property
    def is_authenticated(self):
        """Always return True for actual Master users"""
        return True

    def get_short_name(self):
        """Return the short name for the user"""
        return self.username

    def get_full_name(self):
        """Return the full name for the user (username in this case)"""
        return self.username
