from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify

from orbit.models import Orbit
from participant.models import Participant


class Topic(models.Model):
    about = models.ForeignKey(
        Participant,
        related_name='topics_about',
        on_delete=models.CASCADE,
        verbose_name=_("Participant"),
        help_text=_("The participant about we study")
    )

    # Many-to-many relationship for participants studying this topic
    studying_participants = models.ManyToManyField(
        Participant,
        related_name='studying_topics',
        blank=True,
        verbose_name=_("Studying Participants"),
        help_text=_("Participants who are studying about this participant")
    )

    # Many-to-many relationship for boss participants
    bosses = models.ManyToManyField(
        Participant,
        related_name='boss_topics',
        blank=True,
        verbose_name=_("Bosses"),
        help_text=_("Participants who are bosses for this topic")
    )

    title = models.CharField(
        max_length=100,
        verbose_name=_("Title"),
        help_text=_("Enter a concise title for the topic (max 100 characters)")
    )

    description = models.TextField(
        verbose_name=_("Description"),
        help_text=_("Detailed description of the topic")
    )

    orbit = models.ForeignKey(
        Orbit,
        related_name='topics',
        on_delete=models.CASCADE,
        verbose_name=_("Orbit"),
        help_text=_("The Orbit where the topic belongs")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    # Additional useful fields
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Designates whether this topic is active and visible")
    )

    slug = models.SlugField(
        max_length=105,
        unique=True,
        blank=True,
        verbose_name=_("Slug"),
        help_text=_("URL-friendly version of the title (auto-generated)")
    )

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['created_at']),
            models.Index(fields=['about', 'created_at']),
            models.Index(fields=['is_active']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['about', 'title'],
                name='unique_topic_per_participant'
            )
        ]

    def __str__(self):
        return f"{self.title} - About: {self.about.nickname}"

    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
            # Ensure uniqueness
            original_slug = self.slug
            counter = 1
            while Topic.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1

        self.full_clean()
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        if len(self.title.strip()) < 5:
            raise ValidationError({
                'title': _("Title must be at least 5 characters long.")
            })
        if len(self.description.strip()) < 10:
            raise ValidationError({
                'description': _("Description must be at least 10 characters long.")
            })

    @property
    def studying_participants_count(self):
        """Return the number of participants studying this topic"""
        return self.studying_participants.count()

    @property
    def bosses_count(self):
        """Return the number of boss participants for this topic"""
        return self.bosses.count()

    @property
    def question_count(self):
        """Return the number of questions in this topic"""
        return self.questions.count()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('topics:topic_detail', kwargs={'slug': self.slug})

    def activate(self):
        """Activate the topic"""
        self.is_active = True
        self.save()

    def deactivate(self):
        """Deactivate the topic"""
        self.is_active = False
        self.save()



class Question(models.Model):
    question_text = models.TextField(
        verbose_name=_("Question Text"),
        help_text=_("Enter your question here")
    )

    topic = models.ForeignKey(
        Topic,
        related_name='questions',
        on_delete=models.CASCADE,
        verbose_name=_("Topic"),
        help_text=_("The topic this question belongs to")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    # Additional useful fields
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Active"),
        help_text=_("Designates whether this question is active")
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Order"),
        help_text=_("Order in which questions should be displayed")
    )

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['topic', 'created_at']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"Q: {self.question_text[:50]}..." if len(self.question_text) > 50 else f"Q: {self.question_text}"

    def clean(self):
        super().clean()
        if len(self.question_text.strip()) < 10:
            raise ValidationError({
                'question_text': _("Question must be at least 10 characters long.")
            })

    @property
    def answer_count(self):
        """Return the number of answers for this question"""
        return self.answers.count()

    @property
    def short_question_text(self):
        """Return shortened version of question text"""
        return self.question_text[:100] + "..." if len(self.question_text) > 100 else self.question_text


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        related_name='answers',
        on_delete=models.CASCADE,
        verbose_name=_("Question"),
        help_text=_("The question this answer belongs to")
    )

    answer_text = models.TextField(
        verbose_name=_("Answer Text"),
        help_text=_("Enter your answer here")
    )

    # Add participant field - if null, answer is generated by admin
    participant = models.ForeignKey(
        Participant,
        related_name='answers',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Answered By"),
        help_text=_("Participant who provided this answer (leave blank for admin-generated answers)")
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    # Additional useful fields
    is_correct = models.BooleanField(
        default=False,
        verbose_name=_("Correct Answer"),
        help_text=_("Designates whether this is the correct answer")
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Order"),
        help_text=_("Order in which answers should be displayed")
    )

    class Meta:
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")
        ordering = ['order', 'created_at']
        indexes = [
            models.Index(fields=['question', 'created_at']),
            models.Index(fields=['is_correct']),
            models.Index(fields=['participant']),
        ]

    def __str__(self):
        participant_name = self.participant.nickname if self.participant else "Admin"
        return f"A: {self.answer_text[:50]}... by {participant_name}"

    def clean(self):
        super().clean()
        if len(self.answer_text.strip()) < 5:
            raise ValidationError({
                'answer_text': _("Answer must be at least 5 characters long.")
            })

    @property
    def short_answer_text(self):
        """Return shortened version of answer text"""
        return self.answer_text[:100] + "..." if len(self.answer_text) > 100 else self.answer_text

    @property
    def answered_by_display(self):
        """Return display name for who answered"""
        if self.participant:
            return f"{self.participant.nickname}"
        return "Admin"

    @property
    def is_admin_generated(self):
        """Check if answer was generated by admin"""
        return self.participant is None

    def save(self, *args, **kwargs):
        # If marking this answer as correct, ensure only one correct answer per question
        if self.is_correct:
            Answer.objects.filter(question=self.question, is_correct=True).update(is_correct=False)
        super().save(*args, **kwargs)
