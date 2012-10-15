from django.contrib.auth.models import Group, User
from django.db import models
from registration.signals import user_registered

class UserProfile(models.Model):
    SEX_CHOICES = (('F', 'Female'), ('M', 'Male'))
    user = models.OneToOneField(User)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True, null=True)
    dob = models.DateField('Date of Birth', blank=True, null=True)
    picture = models.ImageField('Profile Picture', upload_to='profile_picture', blank=True)

# When creating a user, add them to citizen group
def create_user_profile(sender, user, request, **kwargs):
    UserProfile.objects.create(user=user)
    group = Group.objects.get(name="Citizen")
    user.groups.add(group)
    user.save()

user_registered.connect(create_user_profile)
