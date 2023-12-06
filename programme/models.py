from django.db import models
from django.db.models.deletion import CASCADE
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
import os
import string
import random
from PIL import Image, ImageDraw, ImageFont
import warnings

# Create your models here.

def renommer_image(instance,filename):
	upload_to = 'image/'
	ext = filename.split('.')[-1]
	if instance.user.username:
		filename = "matiere/{}.{}".format(instance.matiere.nom,ext)
		return os.path.join(upload_to,filename)


def generate_image(module, ecole, niveau, annee):
    upload_to = 'image/'
    # Générer un nom d'image unique
    #nom_template = "template.png"
    nom_template = os.path.join(os.getcwd(),"media","miniatures","template.png")

    # Charger l'image de template
    img = Image.open(nom_template)
    draw = ImageDraw.Draw(img)
    font_path = os.path.join(os.getcwd(), "media", "font", "Montserrat-Regular.ttf")
    fnt_pensee = ImageFont.truetype(font_path, 14)
    fnt_auteur = ImageFont.truetype(font_path, 14)

    # Diviser le texte en lignes
    line_width = 1000
    lines = []
    line = ''

    # Draw the 'module' on the first line
    line += module
    lines.append(line)

    # Draw the 'ecole' on the second line
    line = ecole
    lines.append(line)

    # Combine 'niveau' and 'annee' on the same line
    line = f"Niveau: {niveau} - Année: {annee}"
    lines.append(line)

    # Dessiner les lignes de texte centrées verticalement
    y = img.size[1] // 2 - fnt_pensee.getbbox('\n')[1] * len(lines) // 2
    interline_spacing = 20  # Adjust the interline spacing here
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', category=DeprecationWarning)
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=fnt_pensee)
            w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
            draw.text(((img.size[0] - w) // 2, y), line, font=fnt_pensee, fill=(232, 30, 37))
            y += h + interline_spacing

    # Dessiner les informations
    info_text = f"Module: {module}\nEcole: {ecole}\nNiveau: {niveau}\nAnnée: {annee}"
    info_font_size = 40
    info_font = ImageFont.truetype(font_path, info_font_size)
    info_lines = info_text.split('\n')
    info_y = 1000
    interline_spacing = 10  # Adjust the interline spacing here
    for line in info_lines:
        draw.text((100, info_y), line, font=info_font, fill=(232, 30, 37))
        info_y += info_font_size + interline_spacing

    nom_image = os.path.join(os.getcwd(), "media","miniatures",f"{module}_{ecole}_{niveau}{annee}.png")

    # Enregistrer l'image
    img.save(nom_image, "PNG", quality=100, optimize=True, encoding='utf-8')
    print(nom_image)
    return nom_image


class Categories(models.Model):
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
    categorie = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='matiere')
    image = models.ImageField(upload_to="Matiere", blank=True)
    description = models.TextField(max_length=500)
    
    def __str__(self):
        return self.nom


    def save(self, *args, **kwargs):
        self.slug = slugify(self.nom)  
        super().save(*args, **kwargs)  

class Epreuve(models.Model):
    epreuve_id = models.CharField(unique=True, max_length=40)
    nom = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    categorie = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='epreuve')
    ecole = models.CharField(max_length=40)
    niveau = models.PositiveIntegerField()
    annee = models.PositiveIntegerField()
    description = models.TextField(max_length=500)
    miniature = models.ImageField(upload_to='image/', blank=True)
    pdf = models.FileField(upload_to="PDF", null=True, blank=True, verbose_name="Epreuve en pdf")

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        self.slug = slugify(self.nom)

        if not self.miniature:  # Only generate the image if it's not set already
            module = self.nom
            ecole = self.ecole
            niveau = self.niveau
            annee = self.annee
            image_path = generate_image(module, ecole, niveau, annee)
            # Get the relative path from the 'media' directory
            relative_path = os.path.relpath(image_path, 'media')

            # Convert backslashes to forward slashes
            relative_path = relative_path.replace('\\', '/')
            self.miniature = relative_path

        super().save(*args, **kwargs)

class Lesson(models.Model):
    lesson_id = models.CharField(unique=True, max_length=40)
    categorie = models.ForeignKey(Categories, on_delete=models.CASCADE)
    creer_par = models.ForeignKey(User, on_delete=models.CASCADE) 
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='lesson')
    nom = models.CharField(max_length=100) 
    slug = models.SlugField(blank=True, null=True)
    position = models.PositiveSmallIntegerField(verbose_name='chapitre no')  
    video = models.FileField(upload_to="Video", null=True, blank=True, verbose_name="cours en Video")
    fpe = models.FileField(upload_to="FPE", null=True, blank=True, verbose_name="fiche de presentation")
    pdf = models.FileField(upload_to="PDF", null=True, blank=True, verbose_name="Cours en pdf")
    niveaucompetence = models.CharField(max_length=20, choices=[('debutant', 'Debutant'), ('intermediaire', 'Intermediaire'), ('avance', 'Avance')],default='debutant')
    payant = models.BooleanField(default=False)
    langue = models.CharField(max_length=20, choices=[('toutes_langues', 'Toutes les langues'), ('anglais', 'Anglais'), ('francais', 'Français')],default='toutes_langues')


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