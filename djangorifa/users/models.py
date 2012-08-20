from django.contrib.auth.models import User
from django.db import models
from registration.signals import user_registered

class UserProfile(models.Model):
    SEX_CHOICES = (('F', 'Female'), ('M', 'Male'))
    user = models.OneToOneField(User)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True, null=True)
    dob = models.DateField('Date of Birth', blank=True, null=True)
    picture = models.ImageField('Profile Picture', upload_to='profile_picture', blank=True)

    def is_worker(self):
        return hasattr(self, 'workerprofile')

class WorkerProfile(UserProfile):
    deposit = models.DecimalField(decimal_places=2, max_digits=9, default=0)

def create_user_profile(sender, user, request, **kwargs):
    # If they are applying to be a worker, create the correct profile
    worker = request.POST.get('worker')
    if worker:
        WorkerProfile.objects.create(user=user)
    else:
        UserProfile.objects.create(user=user)

user_registered.connect(create_user_profile)
