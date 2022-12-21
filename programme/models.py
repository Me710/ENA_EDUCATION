from django.db import models
from django.db.models.deletion import CASCADE
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

def renommer_image(instance,filename):
	upload_to = 'image/'
	ext = filename.split('.')[-1]
	if instance.user.username:
		filename = "matiere/{}.{}".format(instance.matiere.nom,ext)
		return os.path.join(upload_to,filename)

class Niveaux(models.Model):
    nom = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField()


    def __str__(self):
        return self.nom


    def save(self, *args, **kwargs):
        self.slug = slugify(self.nom)  
        super().save(*args, **kwargs)  


class Matiere(models.Model):
    matiere_id = models.CharField(unique=True, max_length=40)
    nom = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    niveau = models.ForeignKey(Niveaux, on_delete=models.CASCADE, related_name='matiere')
    image = models.ImageField(upload_to="Matiere", blank=True)
    description = models.TextField(max_length=500)


    def __str__(self):
        return self.nom


    def save(self, *args, **kwargs):
        self.slug = slugify(self.nom)  
        super().save(*args, **kwargs)  

class Lesson(models.Model):
    lesson_id = models.CharField(unique=True, max_length=40)
    niveau = models.ForeignKey(Niveaux, on_delete=models.CASCADE)
    creer_par = models.ForeignKey(User, on_delete=models.CASCADE) 
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='lesson')
    nom = models.CharField(max_length=100) 
    slug = models.SlugField(blank=True, null=True)
    position = models.PositiveSmallIntegerField(verbose_name='chapitre no')  
    video = models.FileField(upload_to="Video", null=True, blank=True, verbose_name="cours en Video")
    fpe = models.FileField(upload_to="FPE", null=True, blank=True, verbose_name="fiche de presentation")
    pdf = models.FileField(upload_to="PDF", null=True, blank=True, verbose_name="Cours en pdf")

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.nom


    def save(self, *args, **kwargs):
        self.slug = slugify(self.nom)  
        super().save(*args, **kwargs)  

    def get_absolute_url(self):
        return reverse("programme:lessonlist", kwargs={"slug": self.matiere.slug, "niveau": self.niveau.slug})


class Commentaire(models.Model):
    nom_lesson = models.ForeignKey(Lesson, null=True, on_delete=models.CASCADE, related_name='comments')
    nom_comm = models.CharField(max_length=100, blank=True)
    # reponse = models.ForeignKey('Commentaire', null=True, blank=True, on_delete=models.CASCADE, related_name='reponses')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    corps = models.TextField(max_length=500)
    date_added = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.nom_comm = slugify("commente par " + str(self.auteur) + "a " + str(self.date_added) )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom_comm

    class Meta:
        ordering = ['-date_added']        


class Reponse(models.Model):
    nom_comm = models.ForeignKey(Commentaire, on_delete=models.CASCADE, related_name='reponses')      
    corps = models.TextField(max_length=500)  
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "reponse a" + str(self.nom_comm.nom_comm)