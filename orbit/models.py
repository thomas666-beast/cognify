import uuid
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils.text import slugify


class Orbit(models.Model):
    # Primary key - good use of UUID
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name=_("ID"),
        help_text=_("Unique identifier for the orbit")
    )

    # Name field with enhanced validation
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_("Orbit Name"),
        help_text=_("Required. 100 characters or fewer. Unique name for the orbit."),
        validators=[
            MinLengthValidator(
                3,
                _("Orbit name must be at least 3 characters long.")
            ),
            RegexValidator(
                regex=r'^[a-zA-Z0-9\s\-_\.]+\Z',
                message=_("Orbit name can only contain letters, numbers, spaces, hyphens, underscores, and dots."),
            )
        ],
        error_messages={
            'unique': _("An orbit with this name already exists."),
        }
    )

    # Slug field for SEO-friendly URLs
    slug = models.SlugField(
        max_length=110,
        unique=True,
        blank=True,
        verbose_name=_("Slug"),
        help_text=_("URL-friendly version of the name (auto-generated)")
    )

    # Description field for additional context
    description = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=_("Description"),
        help_text=_("Optional. Brief description of the orbit (max 500 characters).")
    )

    # Status field to manage orbit lifecycle
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('archived', _('Archived')),
        ('draft', _('Draft')),
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active',
        verbose_name=_("Status"),
        help_text=_("Current status of the orbit")
    )

    # Order field for manual sorting
    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Display Order"),
        help_text=_("Order in which orbits should be displayed (lower numbers first)")
    )

    # Color field for UI differentiation (optional)
    color = models.CharField(
        max_length=7,
        default='#3B82F6',  # Blue color
        verbose_name=_("Color"),
        help_text=_("Hex color code for the orbit (e.g., #3B82F6)")
    )

    # Icon field for visual representation (optional)
    icon = models.CharField(
        max_length=50,
        blank=True,
        verbose_name=_("Icon"),
        help_text=_("Optional. Icon class name (e.g., 'fa-globe', 'bi-orbit')")
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created At")
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Updated At")
    )

    class Meta:
        verbose_name = _("Orbit")
        verbose_name_plural = _("Orbits")
        ordering = ['order', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['order']),
            models.Index(fields=['created_at']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_orbit_name'
            ),
            models.UniqueConstraint(
                fields=['slug'],
                name='unique_orbit_slug'
            ),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Override save to auto-generate slug and validate data"""
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = self.generate_slug()

        # Clean and validate before saving
        self.full_clean()
        super().save(*args, **kwargs)

    def generate_slug(self):
        """Generate a unique slug from the name"""
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1

        # Ensure slug uniqueness
        while Orbit.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug

    def clean(self):
        """Custom validation"""
        super().clean()

        # Clean name by stripping whitespace
        if self.name:
            self.name = self.name.strip()

        # Validate color format if provided
        if self.color and not self.is_valid_hex_color(self.color):
            raise ValidationError({
                'color': _("Enter a valid hex color code (e.g., #3B82F6).")
            })

    @staticmethod
    def is_valid_hex_color(color):
        """Validate hex color format"""
        import re
        pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        return re.match(pattern, color) is not None

    def get_absolute_url(self):
        """Return URL for orbit detail view"""
        return reverse('orbit-detail', kwargs={'slug': self.slug})

    @property
    def is_active(self):
        """Check if orbit is active"""
        return self.status == 'active'

    @property
    def display_name(self):
        """Return display name with status indicator if not active"""
        if self.status != 'active':
            return f"{self.name} ({self.get_status_display()})"
        return self.name

    def activate(self):
        """Activate the orbit"""
        self.status = 'active'
        self.save()

    def deactivate(self):
        """Deactivate the orbit"""
        self.status = 'inactive'
        self.save()

    def archive(self):
        """Archive the orbit"""
        self.status = 'archived'
        self.save()

    class Manager(models.Manager):
        def active(self):
            """Return active orbits only"""
            return self.filter(status='active')

        def inactive(self):
            """Return inactive orbits only"""
            return self.filter(status='inactive')

        def archived(self):
            """Return archived orbits only"""
            return self.filter(status='archived')

        def by_status(self, status):
            """Return orbits by specific status"""
            return self.filter(status=status)

        def search(self, query):
            """Search orbits by name or description"""
            return self.filter(
                models.Q(name__icontains=query) |
                models.Q(description__icontains=query)
            )

    # Custom manager
    objects = Manager()


# Proxy models for specific use cases
class ActiveOrbit(Orbit):
    """Proxy model for active orbits only"""

    class Meta:
        proxy = True
        verbose_name = _("Active Orbit")
        verbose_name_plural = _("Active Orbits")
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        """Ensure proxy model instances are always active"""
        self.status = 'active'
        super().save(*args, **kwargs)


class ArchivedOrbit(Orbit):
    """Proxy model for archived orbits only"""

    class Meta:
        proxy = True
        verbose_name = _("Archived Orbit")
        verbose_name_plural = _("Archived Orbits")
        ordering = ['-updated_at']


# Example of how you might extend this for specific functionality
class OrbitStatistics(models.Model):
    """Optional: Model to track orbit statistics"""
    orbit = models.OneToOneField(
        Orbit,
        on_delete=models.CASCADE,
        related_name='statistics'
    )
    participant_count = models.PositiveIntegerField(default=0)
    topic_count = models.PositiveIntegerField(default=0)
    last_activity = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("Orbit Statistics")
        verbose_name_plural = _("Orbit Statistics")

    def __str__(self):
        return f"Statistics for {self.orbit.name}"
