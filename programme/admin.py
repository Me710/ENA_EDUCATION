from django.contrib import admin
from .models import Categories, Matiere, Lesson, Commentaire, Reponse,Epreuve

# Register your models here.

admin.site.register(Categories)
admin.site.register(Matiere)
admin.site.register(Lesson)
admin.site.register(Commentaire)
admin.site.register(Reponse)
admin.site.register(Epreuve)
