from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from decimal import Decimal
from django.contrib.auth.models import User


class Company(models.Model):
    class Meta:
        verbose_name_plural = "companies"

    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    company = models.ForeignKey('projects.Company', on_delete=models.PROTECT, related_name='projects')

    title = models.CharField('Project title', max_length=128)
    start_date = models.DateField('Project start date', blank=True, null=True)
    end_date = models.DateField('Project end date', blank=True, null=True)

    estimated_design = models.PositiveSmallIntegerField('Estimated design hours')
    actual_design = models.DecimalField('Actual design hours', default=0, max_digits=5, decimal_places=2,
                                        validators=[MinValueValidator(Decimal('0.00'))])

    estimated_development = models.PositiveSmallIntegerField('Estimated development hours')
    actual_development = models.DecimalField('Actual development hours', default=0, max_digits=5, decimal_places=2,
                                             validators=[MinValueValidator(Decimal('0.00'))])

    estimated_testing = models.PositiveSmallIntegerField('Estimated testing hours')
    actual_testing = models.DecimalField('Actual testing hours', default=0, max_digits=5, decimal_places=2,
                                         validators=[MinValueValidator(Decimal('0.00'))])
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project-update', kwargs={'pk': self.pk, 'slug': slugify(self.title)})

    @property
    def has_ended(self):
        return self.end_date is not None and self.end_date < timezone.now().date()

    @property
    def total_estimated_hours(self):
        return self.estimated_design + self.estimated_development + self.estimated_testing

    @property
    def total_actual_hours(self):
        return self.actual_design + self.actual_development + self.actual_testing

    @property
    def is_over_budget(self):
        return self.total_actual_hours > self.total_estimated_hours


class LogActualHourEdit(models.Model):
    class Meta:
        verbose_name_plural = "Log actual hour edits"

    changed_by = models.ForeignKey(User, related_name='log_changed_by', on_delete=models.CASCADE)
    changed_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    initial_value = models.DecimalField(max_digits=5, decimal_places=2)
    change_delta = models.DecimalField(max_digits=5, decimal_places=2)
    final_value = models.DecimalField(max_digits=5, decimal_places=2)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
