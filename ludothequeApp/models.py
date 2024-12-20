from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    phone_nbr = models.CharField(max_length=10, default='0')

# Model jeu de reference
class jeu_de_reference(models.Model):
    nom = models.CharField(max_length=250)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Jeu de Référence : {self.nom}"

# Model piece standard d'un jeu de reference
class piece_standard(models.Model):
    jeu = models.ForeignKey(jeu_de_reference, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    essentiel = models.BooleanField(default=True)

    def __str__(self):
        return f"Piece standard : {self.nom} de {self.jeu}"

#Model exemplaire d'un reference
class exemplaire(models.Model):
    jeu = models.ForeignKey(jeu_de_reference, on_delete=models.CASCADE)
    nom = models.CharField(max_length=250, default='None')
    jouable = models.BooleanField(default=True)
    dispo = models.BooleanField(default=True)

    def __str__(self):
        return f"Exemplaire : {self.nom} de {self.jeu}"

# Model piece d'un exemplaire
class piece_exemplaire(models.Model):
    ex = models.ForeignKey(exemplaire, on_delete=models.CASCADE)
    pis = models.ForeignKey(piece_standard, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    presente = models.BooleanField(default=True)

    def __str__(self):
        return f"Piece exemplaire : {self.nom} de {self.ex}"

# Model des Prets des jeux
class pret(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    ex = models.ForeignKey(exemplaire, on_delete=models.CASCADE)
    date_emprunt = models.DateTimeField(auto_now_add=True)
    date_retour = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"L'{self.ex} est preté par : {self.id_user} le {self.date_emprunt}, le retour sera {self.date_retour}"
    
# Model pour l'historique des fussion
class fussion_historique(models.Model):
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    ex1 = models.ForeignKey(exemplaire, related_name='ex1', on_delete=models.CASCADE)
    ex2 = models.ForeignKey(exemplaire, related_name='ex2', on_delete=models.CASCADE)
    total = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.ex1} a été fussionner avec {self.ex2}, le nombre de piéces fussionnés {self.total}"
    

