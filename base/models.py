from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/emptyprofpic.png')
    dark_mode = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if not hasattr(instance, 'profile'):
            Profile.objects.create(user=instance)
    instance.profile.save()

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_results')
    date_taken = models.DateTimeField(auto_now_add=True)
    top_field_1 = models.CharField(max_length=100)
    top_field_2 = models.CharField(max_length=100, blank=True, null=True)
    score_field_1 = models.IntegerField()
    score_field_2 = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s result: {self.top_field_1}"