from django.db import models
from django.contrib.auth.models import User
import os

def renommer_image(instance,filename):
	upload_to = 'static/img/hero'
	#ext = filename.split('.')[-1]
	#if instance.user.username:
	#	filename = "photo_profile/{}.{}".format(instance.user.username,ext)
	return os.path.join(upload_to,filename)


class Profile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	bio = models.CharField(max_length=150,blank=True)
	photo_profile = models.ImageField(upload_to=renommer_image,blank=True)

	etudiant = 'etudiant'
	enseignant = 'enseignant'

	type_user = [
		(etudiant,'etudiant'),(enseignant,'enseignant')

	]
	type_profile = models.CharField(max_length=100,choices=type_user)

	def __str__(self):
		return self.user.username


# Create your models here.
