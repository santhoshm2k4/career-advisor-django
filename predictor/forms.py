# predictor/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm # Import base form
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class JobPredictionForm(forms.Form):
    """Dynamically creates RadioSelect fields for job prediction features."""

    def __init__(self, *args, **kwargs):
        features = kwargs.pop('features', [])
        categories = kwargs.pop('categories', [])
        super().__init__(*args, **kwargs)

        # Create choices suitable for ChoiceField/RadioSelect: [(value, display), ...]
        # Exclude the placeholder '-- Select Level --' as radios should always have a default selection conceptually
        category_choices = [(cat, cat.title()) for cat in categories]

        # Dynamically add a ChoiceField using RadioSelect for each feature
        for feature in features:
            field_name = feature
            self.fields[field_name] = forms.ChoiceField(
                label=feature.title(),
                choices=category_choices, # Use only the actual categories
                required=True,
                # Use RadioSelect widget
                widget=forms.RadioSelect(attrs={
                    'class': 'level-radio visually-hidden' # Hide actual radio, use class for JS/CSS
                    })
            )


class DegreePredictionForm(forms.Form):
    """Dynamically creates BooleanFields for degree prediction interests."""

    def __init__(self, *args, **kwargs):
        # Pop custom arguments before calling super
        features = kwargs.pop('features', [])
        super().__init__(*args, **kwargs)

        # Dynamically add a BooleanField (checkbox) for each interest
        for feature in features:
            field_name = feature
            self.fields[field_name] = forms.BooleanField(
                label=feature.title(),
                required=False, # Not required to check an interest
                widget=forms.CheckboxInput(attrs={
                    'class': 'interest-checkbox visually-hidden' # Keep visually hidden
                })
            )

class ProfileUpdateForm(forms.ModelForm):
    """Form for users to update their profile information."""
    class Meta:
        model = Profile
        fields = ['full_name'] # List fields the user can edit
        # Add more fields here if you add them to the Profile model
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            # Add widgets for other fields if needed
        }

class CustomUserCreationForm(UserCreationForm):
    # Add an explicit EmailField
    email = forms.EmailField(
        required=True, # Make email required during registration
        widget=forms.EmailInput(attrs={'class': 'form-control'}) # Apply Bootstrap class
    )

    class Meta(UserCreationForm.Meta): # Inherit Meta from base form
        model = User
        # Specify fields to include: inherit username/password fields AND add email
        fields = UserCreationForm.Meta.fields + ('email',)