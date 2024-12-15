from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title


# Profile model for user-specific information (including role)
class Profile(models.Model):
    ROLE_CHOICES = [
        ('relief_recipient', 'Relief Recipient'),
        ('consultant', 'Consultant'),
        ('administrator', 'Administrator'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='relief_recipient')
    full_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username} ({self.role})"


# Appointment model for booking and managing appointments
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    relief_recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="appointments_as_recipient",
        limit_choices_to={'profile__role': 'relief_recipient'}
    )
    consultant = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="appointments_as_consultant",
        limit_choices_to={'profile__role': 'consultant'}
    )
    date_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    def __str__(self):
        return f"Appointment with {self.relief_recipient} and {self.consultant} on {self.date_time}"


# Administrator-specific functionality for managing users
class AdministratorAction(models.Model):
    administrator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="actions",
        limit_choices_to={'profile__role': 'administrator'}
    )
    user_affected = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="managed_by_admin"
    )
    action_taken = models.CharField(max_length=255)
    action_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.administrator.username} managed {self.user_affected.username}"
