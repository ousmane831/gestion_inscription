from django.db import models
from django.core.exceptions import ValidationError

# ------------------------------
# Modèle Département
# ------------------------------
class Departement(models.Model):
    nom = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"

    def __str__(self):
        return self.nom

# ------------------------------
# Modèle Filière
# ------------------------------
class Filiere(models.Model):
    nom = models.CharField(max_length=100)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"

    def __str__(self):
        return f"{self.nom} ({self.departement.nom})"

# ------------------------------
# Modèle Étudiant
# ------------------------------
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

    class Meta:
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"

    def __str__(self):
        return f"{self.prenom} {self.nom} ({'Inscrit' if self.inscrit else 'Non inscrit'})"

    def clean(self):
        # ✅ Vérification : la filière doit appartenir au département choisi
        if self.filiere.departement != self.departement:
            raise ValidationError("La filière ne correspond pas au département sélectionné.")

    def save(self, *args, **kwargs):
        self.full_clean()  # ✅ Pour exécuter clean() avant l’enregistrement
        super().save(*args, **kwargs)

    @property
    def date_naissance_formattee(self):
        return self.date_naissance.strftime("%d/%m/%Y")
