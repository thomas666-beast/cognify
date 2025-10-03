import uuid
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Participant(models.Model):
    # Primary key - good use of UUID
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("ID")
    )

    # Nickname with validation
    nickname = models.CharField(
        max_length=120,
        unique=True,
        verbose_name=_("Nickname"),
        help_text=_("Required. 120 characters or fewer. Letters, digits and @/./+/-/_ only."),
        validators=[
            MinLengthValidator(3, _("Nickname must be at least 3 characters long.")),
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message=_(
                    "Enter a valid nickname. This value may contain only letters, numbers, and @/./+/-/_ characters."),
            )
        ],
        error_messages={
            'unique': _("A participant with that nickname already exists."),
        }
    )

    # Personal name fields
    firstname = models.CharField(
        max_length=120,
        verbose_name=_("First Name"),
        help_text=_("Enter your legal first name."),
        validators=[
            MinLengthValidator(2, _("First name must be at least 2 characters long.")),
            RegexValidator(
                regex=r'^[a-zA-Z\s\-\.\']+\Z',
                message=_("First name can only contain letters, spaces, hyphens, dots, and apostrophes."),
            )
        ]
    )

    lastname = models.CharField(
        max_length=120,
        verbose_name=_("Last Name"),
        help_text=_("Enter your legal last name."),
        validators=[
            MinLengthValidator(2, _("Last name must be at least 2 characters long.")),
            RegexValidator(
                regex=r'^[a-zA-Z\s\-\.\']+\Z',
                message=_("Last name can only contain letters, spaces, hyphens, dots, and apostrophes."),
            )
        ]
    )

    # Position field with choices for better data consistency
    POSITION_CHOICES = [
        ('developer', _('Developer')),
        ('designer', _('Designer')),
        ('manager', _('Manager')),
        ('analyst', _('Analyst')),
        ('researcher', _('Researcher')),
        ('student', _('Student')),
        ('professor', _('Professor')),
        ('other', _('Other')),
    ]

    position = models.CharField(
        max_length=120,
        choices=POSITION_CHOICES,
        verbose_name=_("Position/Role"),
        help_text=_("Select your primary role or position."),
        default='other'
    )

    # Additional useful fields
    email = models.EmailField(
        verbose_name=_("Email Address"),
        unique=True,
        blank=True,
        null=True,
        help_text=_("Optional. Your email address for notifications.")
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Designates whether this participant is active.")
    )

    bio = models.TextField(
        verbose_name=_("Biography"),
        max_length=500,
        blank=True,
        help_text=_("Optional. Tell us about yourself (max 500 characters).")
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date Joined")
    )

    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Updated")
    )

    class Meta:
        verbose_name = _("Participant")
        verbose_name_plural = _("Participants")
        ordering = ['lastname', 'firstname']
        indexes = [
            models.Index(fields=['nickname']),
            models.Index(fields=['lastname', 'firstname']),
            models.Index(fields=['position']),
            models.Index(fields=['is_active']),
            models.Index(fields=['date_joined']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['firstname', 'lastname'],
                name='unique_full_name',
                condition=models.Q(is_active=True),
            )
        ]

    def __str__(self):
        return f"{self.nickname} - {self.get_full_name()}"

    def clean(self):
        """Custom validation"""
        super().clean()

        # Ensure first and last names are properly capitalized
        if self.firstname:
            self.firstname = self.firstname.strip().title()
        if self.lastname:
            self.lastname = self.lastname.strip().title()
        if self.nickname:
            self.nickname = self.nickname.strip()

    def save(self, *args, **kwargs):
        """Override save to include validation"""
        self.full_clean()
        super().save(*args, **kwargs)

    def get_full_name(self):
        """Return the full name of the participant"""
        return f"{self.firstname} {self.lastname}".strip()

    def get_short_name(self):
        """Return a short name for the participant"""
        return self.nickname

    @property
    def display_name(self):
        """Return display name (full name if available, otherwise nickname)"""
        full_name = self.get_full_name()
        return full_name if full_name.strip() else self.nickname

    @property
    def topic_count(self):
        """Return the number of topics created by this participant"""
        if hasattr(self, 'topics'):
            return self.topics.count()
        return 0

    def get_absolute_url(self):
        """Return URL for participant detail view"""
        from django.urls import reverse
        return reverse('participant-detail', kwargs={'pk': self.pk})

    def deactivate(self):
        """Deactivate the participant (soft delete)"""
        self.is_active = False
        self.save()

    def activate(self):
        """Activate the participant"""
        self.is_active = True
        self.save()

    class Manager(models.Manager):
        def active(self):
            return self.filter(is_active=True)

        def by_position(self, position):
            return self.filter(position=position, is_active=True)

        def search(self, query):
            return self.filter(
                models.Q(nickname__icontains=query) |
                models.Q(firstname__icontains=query) |
                models.Q(lastname__icontains=query) |
                models.Q(email__icontains=query),
                is_active=True
            )

    # Custom manager
    objects = Manager()


# Optional: Proxy model for specific use cases
class ActiveParticipant(Participant):
    """Proxy model for active participants only"""

    class Meta:
        proxy = True
        verbose_name = _("Active Participant")
        verbose_name_plural = _("Active Participants")

    def save(self, *args, **kwargs):
        """Ensure proxy model instances are always active"""
        self.is_active = True
        super().save(*args, **kwargs)
