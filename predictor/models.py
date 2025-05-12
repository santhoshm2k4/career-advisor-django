# predictor/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
# NEW Imports for Profile linkage via Signals
from django.db.models.signals import post_save
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL

# --- Keep existing JobPredictionRecord and DegreePredictionRecord models ---
class JobPredictionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_predictions')
    timestamp = models.DateTimeField(default=timezone.now)
    input_features = models.JSONField()
    predicted_role = models.CharField(max_length=255)
    class Meta: ordering = ['-timestamp']
    def __str__(self):
        username = self.user.username if self.user else 'Unknown'
        return f"{username} - Job: {self.predicted_role} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"

class DegreePredictionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='degree_predictions')
    timestamp = models.DateTimeField(default=timezone.now)
    input_features = models.JSONField()
    predicted_degree = models.CharField(max_length=255)
    class Meta: ordering = ['-timestamp']
    def __str__(self):
        username = self.user.username if self.user else 'Unknown'
        return f"{username} - Degree: {self.predicted_degree} ({self.timestamp.strftime('%Y-%m-%d %H:%M')})"

class Profile(models.Model):
    # ... (keep existing fields) ...
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='profile')
    full_name = models.CharField(max_length=100, blank=True, null=True)
    def __str__(self):
        return f"{self.user.username}'s Profile"

# --- Signal to create/update profile automatically (MODIFIED) ---
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create a Profile for a new User, or ensure it exists for updated Users.
    """
    if created:
        # If user was just created, create the profile
        Profile.objects.create(user=instance)
        print(f"Profile created automatically for new user {instance.username}")
    else:
        # If user was updated (e.g., during login), ensure profile exists
        # Use try-except to handle cases where profile might be missing for older users
        try:
            # Attempt to access the related profile. This will raise DoesNotExist if it's missing.
            # We don't necessarily need to save it here unless profile fields could be updated
            # indirectly via the user save, which is uncommon. Saving might be redundant.
            # Let's just ensure it exists.
            profile = instance.profile
            # Optional: If you later add logic that might update Profile via User save, uncomment save:
            # profile.save()
            # print(f"Profile found and saved for user {instance.username}")
        except Profile.DoesNotExist:
            # If profile doesn't exist for an existing user (e.g., created before signals)
            # Create it now.
            Profile.objects.create(user=instance)
            print(f"Profile created on-demand for existing user {instance.username}")