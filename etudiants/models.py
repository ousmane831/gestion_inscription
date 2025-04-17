from django.db import models

# Create your models here.


class Departement(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} ({self.departement.nom})"

class Etudiant(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    filiere = models.ForeignKey(Filiere, on_delete=models.CASCADE)
    matricule = models.CharField(max_length=20, unique=True)
    date_inscription = models.DateField(auto_now_add=True)
    inscrit = models.BooleanField(default=False)  # ✅ Nouveau champ

    def __str__(self):
        return f"{self.prenom} {self.nom} ({'Inscrit' if self.inscrit else 'Non inscrit'})"
