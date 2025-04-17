from django.shortcuts import render, redirect, get_object_or_404
from .models import Etudiant, Departement, Filiere
from django.db.models import Q  # Assurez-vous que Q est importé depuis django.db.models

from .forms import EtudiantForm
from django.contrib.admin.views.decorators import staff_member_required
 #pour proteger l'admin 

from django.contrib.auth.decorators import user_passes_test

def staff_member_required(function=None):
    """
    Décorateur pour vérifier si l'utilisateur est membre du personnel.
    """
    return user_passes_test(lambda user: user.is_staff)(function)


@staff_member_required
def dashboard_admin(request):
    # Calculer des informations comme le nombre d'étudiants inscrits
    total_etudiants = Etudiant.objects.count()
    inscrits = Etudiant.objects.filter(inscrit=True).count()
    non_inscrits = Etudiant.objects.filter(inscrit=False).count()

    context = {
        'total_etudiants': total_etudiants,
        'inscrits': inscrits,
        'non_inscrits': non_inscrits,
        'filieres': Filiere.objects.all(),
    }

    return render(request, 'etudiants/dashboard.html', context)

from django.shortcuts import render
from .models import Etudiant
from django.db.models import Count

#liste des etudiants
@staff_member_required
def liste_etudiants(request):
    statut = request.GET.get('statut')
    recherche = request.GET.get('q')

    etudiants = Etudiant.objects.all().order_by("-date_inscription")

    if statut:
        if statut == 'inscrit':
            etudiants = etudiants.filter(inscrit=True)
        elif statut == 'non_inscrit':
            etudiants = etudiants.filter(inscrit=False)

    if recherche:
        etudiants = etudiants.filter(
            Q(nom__icontains=recherche) | Q(matricule__icontains=recherche)
        )

    return render(request, 'etudiants/liste_etudiants.html', {'etudiants': etudiants})

#views pour changer l'status inscrit ou non inscrit
from django.contrib import messages

@staff_member_required
def modifier_statut_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, pk=etudiant_id)
    
    if request.method == 'POST':
        inscrit = request.POST.get('inscrit') == 'on'
        etudiant.inscrit = inscrit
        etudiant.save()
        messages.success(request, f"Le statut de {etudiant.nom} a été mis à jour.")
        return redirect('liste_etudiants')

    return render(request, 'etudiants/update_status.html', {'etudiant': etudiant})

#views pour ajouter et modifier des etudiant
def ajouter_etudiant(request):
    if request.method == 'POST':
        form = EtudiantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_etudiants')
    else:
        form = EtudiantForm()
    return render(request, 'etudiants/ajouter_etudiant.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Etudiant
from .forms import EtudiantForm  # On va créer ce formulaire

def modifier_etudiant(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    
    if request.method == 'POST':
        form = EtudiantForm(request.POST, instance=etudiant)
        if form.is_valid():
            form.save()
            return redirect('liste_etudiants')  # ou ta vue qui affiche la liste
    else:
        form = EtudiantForm(instance=etudiant)
    
    return render(request, 'etudiants/modifier_etudiant.html', {'form': form})

@staff_member_required
def changer_statut(request, etudiant_id):
    etudiant = get_object_or_404(Etudiant, id=etudiant_id)
    etudiant.inscrit = not etudiant.inscrit  # Inverser le statut d'inscription
    etudiant.save()

    return redirect('etudiants_par_filiere', filiere_id=etudiant.filiere.id)


#afficher les etudiants inscrit ou non inscrit par filier
# views.py

from django.shortcuts import render, get_object_or_404
from .models import Filiere, Etudiant

@staff_member_required
def etudiants_par_filiere(request, filiere_id):
    filiere = get_object_or_404(Filiere, id=filiere_id)
    etudiants = Etudiant.objects.filter(filiere=filiere)  # Assure-toi que l'étudiant a un champ 'filiere'

    context = {
        'filiere': filiere,
        'etudiants': etudiants
    }

    return render(request, 'etudiants/etudiants_par_filiere.html', context)
