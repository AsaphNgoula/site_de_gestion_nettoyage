# blog/proclean/forms.py
from django import forms
from django.core.validators import FileExtensionValidator
from .models import JobApplication

class JobApplicationForm(forms.ModelForm):
    # Champs multiples pour les disponibilités
    DISPONIBILITES_CHOICES = [
        ('soir', 'Soir'),
        ('fin_semaine', 'Fin de semaine'),
        ('temps_partiel', 'Temps partiel'),
        ('temps_plein', 'Temps plein'),
        ('jours', 'Jours'),
    ]
    
    disponibilites = forms.MultipleChoiceField(
        choices=DISPONIBILITES_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Disponibilités *"
    )
    
    # Champs radio personnalisés
    experience_menage = forms.ChoiceField(
        choices=[(True, 'Oui'), (False, 'Non')],
        widget=forms.RadioSelect,
        required=True,
        label="Avez-vous de l'expérience en entretien ménager ? *"
    )
    
    vehicule = forms.ChoiceField(
        choices=[(True, 'Oui'), (False, 'Non')],
        widget=forms.RadioSelect,
        required=True,
        label="Possédez-vous un véhicule ou moyen de transport fiable ? *"
    )
    
    # Validation du fichier
    cv = forms.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx'],
                message="Seuls les fichiers PDF, DOC et DOCX sont acceptés."
            )
        ],
        label="CV *"
    )
    
    class Meta:
        model = JobApplication
        fields = [
            'nom', 'prenom', 'email', 'telephone',
            'region', 'region_autre',
            'disponibilites', 'experience_menage', 'vehicule',
            'cv', 'message', 'consentement'
        ]
        widgets = {
            'region': forms.RadioSelect,
            'message': forms.Textarea(attrs={'rows': 4}),
            'region_autre': forms.Textarea(attrs={'rows': 2}),
        }
    
    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        if cv:
            # Vérifier la taille du fichier (5MB max)
            if cv.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError("Le fichier est trop volumineux (max 5MB).")
        return cv
    
    def clean(self):
        cleaned_data = super().clean()
        region = cleaned_data.get('region')
        region_autre = cleaned_data.get('region_autre')
        
        # Validation: si région = "autre", le champ "autre" est requis
        if region == 'autre' and not region_autre:
            self.add_error('region_autre', "Veuillez préciser votre région.")
        
        # Conversion des choix radio en booléens
        experience_menage = cleaned_data.get('experience_menage')
        vehicule = cleaned_data.get('vehicule')
        
        if experience_menage is not None:
            cleaned_data['experience_menage'] = (experience_menage == 'True')
        
        if vehicule is not None:
            cleaned_data['vehicule'] = (vehicule == 'True')
        
        return cleaned_data