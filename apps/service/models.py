from django.db import models


class Branch(models.Model):
    """Physical Orient Computers showroom/branch."""

    name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    maps_url = models.URLField(blank=True, help_text='Google Maps link')
    hours = models.CharField(max_length=100, default='Sat–Thu: 10am – 8pm')
    off_day = models.CharField(max_length=50, default='Friday', help_text='Weekly Holiday')
    is_flagship = models.BooleanField(default=False)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['display_order']
        verbose_name_plural = 'Branches'

    def __str__(self):
        return self.name


class Complaint(models.Model):
    """Customer warranty inquiry or service complaint."""

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_review', 'In Review'),
        ('resolved', 'Resolved'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    order_reference = models.CharField(max_length=60, blank=True,
                                       help_text='Tracking number or order ID')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.name} – {self.subject}'
