from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.dashboard_admin, name='dashboard_admin'),
    path('filiere/<int:filiere_id>/', views.etudiants_par_filiere, name='etudiants_par_filiere'),
    path('liste_etudiants', views.liste_etudiants, name='liste_etudiants'),
    path('changer-statut/<int:etudiant_id>/', views.modifier_statut_etudiant, name='changer_statut'),
    path('ajouter/', views.ajouter_etudiant, name='ajouter_etudiant'),
    path('modifier/<int:etudiant_id>/', views.modifier_etudiant, name='modifier_etudiant'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='etudiants/login.html'), name='login'),
]