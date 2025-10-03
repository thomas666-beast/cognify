from django.db import models

class AntiSpyQuote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quote[:50]}... - {self.author}"

    class Meta:
        verbose_name = 'Anti Spy Quote'
        verbose_name_plural = 'Anti Spy Quotes'
        ordering = ['-created_at']
