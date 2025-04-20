# init_departements.py

import os
import django

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_inscription.settings')  # change ça avec le nom réel de ton projet
django.setup()

from etudiants.models import Departement, Filiere

# Données des départements et filières
data = {
    "Informatique": ["APD", "DBE", "DFE", "ABD", "ASSC", "RSIOT"],
    "Automobile": ["FCA", "CPA", "EMA", "ELC"]
}

for dept_nom, filieres in data.items():
    departement, created = Departement.objects.get_or_create(nom=dept_nom)
    for filiere_nom in filieres:
        Filiere.objects.get_or_create(nom=filiere_nom, departement=departement)

print("Départements et filières enregistrés avec succès.")
