from django.contrib import admin
from .models import User, jeu_de_reference, exemplaire, piece_standard, piece_exemplaire, pret
# Register your models here.


admin.site.register(User)
admin.site.register(jeu_de_reference)
admin.site.register(exemplaire)
admin.site.register(piece_standard)
admin.site.register(piece_exemplaire)
admin.site.register(pret)