# predictor/views.py

import joblib
import pandas as pd
import numpy as np
import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages # Import messages framework
from .models import JobPredictionRecord, DegreePredictionRecord, Profile # Import the models
from .forms import JobPredictionForm, DegreePredictionForm, ProfileUpdateForm, CustomUserCreationForm # Import forms
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger # Import Paginator classes

# --- Define Paths to Model Artifacts ---
MODEL_DIR_JOB = os.path.join(settings.BASE_DIR, 'ml_models', 'ml_models_job_9k')
MODEL_DIR_DEGREE = os.path.join(settings.BASE_DIR, 'ml_models', 'ml_models_degree')

# --- Global Variables for Loaded Artifacts ---
# Initialize to None, load below
rf_model_job = None
feature_encoder_job = None
target_encoder_job = None
feature_names_job = None
ordinal_categories_job = None

rf_model_degree = None
label_encoder_degree_target = None
feature_names_degree = None

# --- Load Job Predictor Artifacts ---
print("--- Loading Job Predictor Artifacts (dataset9000) ---")
try:
    rf_model_job = joblib.load(os.path.join(MODEL_DIR_JOB, 'rf_model_job_9k.joblib'))
    feature_encoder_job = joblib.load(os.path.join(MODEL_DIR_JOB, 'ordinal_encoder_features_9k.joblib'))
    target_encoder_job = joblib.load(os.path.join(MODEL_DIR_JOB, 'label_encoder_target_role_9k.joblib'))
    feature_names_job = joblib.load(os.path.join(MODEL_DIR_JOB, 'feature_names_9k.joblib'))
    ordinal_categories_job = joblib.load(os.path.join(MODEL_DIR_JOB, 'ordinal_categories_order_9k.joblib'))
    print("--- Job artifacts (dataset9000) loaded successfully. ---")
except FileNotFoundError as e:
    print(f"ERROR loading Job artifacts: {e}. Check path '{MODEL_DIR_JOB}'")
except Exception as e:
    print(f"An unexpected error occurred loading Job artifacts: {e}")

# --- Load Degree Predictor Artifacts ---
print("\n--- Loading Degree Predictor Artifacts ---")
try:
    rf_model_degree = joblib.load(os.path.join(MODEL_DIR_DEGREE, 'rf_degree_model.joblib'))
    label_encoder_degree_target = joblib.load(os.path.join(MODEL_DIR_DEGREE, 'label_encoder_degree_target.joblib'))
    feature_names_degree = joblib.load(os.path.join(MODEL_DIR_DEGREE, 'feature_names_degree.joblib'))
    print("--- Degree artifacts loaded successfully. ---")
except FileNotFoundError as e:
    print(f"ERROR loading Degree artifacts: {e}. Check path '{MODEL_DIR_DEGREE}'")
except Exception as e:
    print(f"An unexpected error occurred loading Degree artifacts: {e}")

print("\n--- All Models and artifacts loading process complete. ---")


# ==============================================================================
#                 Helper Prediction Functions (Defined First)
# ==============================================================================

def predict_job_role(input_data):
    """
    Predicts the job role based on input data using the dataset9000 model.
    Args:
        input_data (dict): Dictionary containing feature names and their string values.
    Returns:
        str: The predicted job role name or an error message starting with "Error:".
    """
    if not all([rf_model_job, feature_encoder_job, target_encoder_job, feature_names_job]):
        print("Error: Job prediction cannot proceed because some artifacts failed to load.")
        return "Error: Job prediction model or encoders not loaded properly."
    try:
        input_df_unordered = pd.DataFrame([input_data])
        for col in feature_names_job:
            if col not in input_df_unordered.columns:
                input_df_unordered[col] = 'Not Interested'
        input_df_ordered = input_df_unordered[feature_names_job]
        # print("Job input DataFrame (Ordered, before encoding):\n", input_df_ordered) # Keep commented unless debugging
        input_encoded = feature_encoder_job.transform(input_df_ordered)
        # print("Encoded Job Input Array:\n", input_encoded) # Keep commented unless debugging
        prediction_encoded = rf_model_job.predict(input_encoded)
        # print("Raw prediction (encoded):", prediction_encoded) # Keep commented unless debugging
        prediction_label = target_encoder_job.inverse_transform(prediction_encoded)
        print("Prediction (label):", prediction_label[0])
        return prediction_label[0]
    except ValueError as e:
        print(f"!ValueError during job prediction!: {e}\nInput: {input_data}")
        return "Error: Invalid input value provided for one or more fields."
    except Exception as e:
        print(f"!Unexpected error during job prediction!: {e}\nInput: {input_data}")
        return "Error: An unexpected error occurred during job prediction processing."


def predict_degree(input_data):
    """
    Predicts the degree program based on interest input data.
    Args:
        input_data (dict): Dictionary containing interest feature names as keys (value 1 if present).
    Returns:
        str: The predicted degree name or an error message starting with "Error:".
    """
    if not all([rf_model_degree, label_encoder_degree_target, feature_names_degree]):
        print("Error: Degree prediction cannot proceed because some artifacts failed to load.")
        return "Error: Degree prediction model or encoders not loaded properly."
    try:
        data_for_prediction = {feature: [0] for feature in feature_names_degree}
        for feature, value in input_data.items():
            if feature in data_for_prediction:
                data_for_prediction[feature][0] = int(value) if value else 0
        input_df = pd.DataFrame.from_dict(data_for_prediction)
        input_df = input_df[feature_names_degree]
        # print("Degree input DataFrame:\n", input_df) # Keep commented unless debugging
        prediction_encoded = rf_model_degree.predict(input_df)
        # print("Raw degree prediction (encoded):", prediction_encoded) # Keep commented unless debugging
        prediction_label = label_encoder_degree_target.inverse_transform(prediction_encoded)
        print("Degree Prediction (label):", prediction_label[0])
        return prediction_label[0]
    except ValueError as e:
        if "contains previously unseen labels" in str(e):
            print(f"!LabelEncoder issue in degree prediction!. Raw prediction: {prediction_encoded}. Error: {e}")
            return "Error: Model predicted an unknown category. Check LabelEncoder consistency."
        else:
            print(f"!ValueError during degree prediction!: {e}\nInput: {input_data}")
            return "Error: Invalid input value provided for degree prediction."
    except Exception as e:
        print(f"!Unexpected error during degree prediction!: {e}\nInput: {input_data}")
        return "Error: An unexpected error occurred during degree prediction processing."


# ==============================================================================
#                         Django View Functions
# ==============================================================================

def index(request):
    """ Redirects users based on authentication status. """
    if request.user.is_authenticated:
        return redirect('predictor:dashboard')
    else:
        return redirect('login')

@login_required
def dashboard(request):
    """ Displays the main dashboard after login. """
    context = {'username': request.user.username}
    return render(request, 'predictor/dashboard.html', context)


@login_required
def predict_job_view(request):
    """Handles the Job Role Prediction page and form submission using Django Forms."""
    # Check resource availability (keep this)
    if not all([feature_names_job, ordinal_categories_job]):
        messages.error(request, "Job prediction resources are not available.")
        return redirect('predictor:dashboard')

    form = None # Initialize form variable

    if request.method == 'POST':
        # Instantiate form with POST data AND dynamic choices
        form = JobPredictionForm(request.POST, features=feature_names_job, categories=ordinal_categories_job)

        if form.is_valid():
            print("Job form is valid. Processing prediction...")
            job_input_data = form.cleaned_data # Use cleaned data
            prediction = predict_job_role(job_input_data)

            # Handle prediction result (keep message logic)
            if prediction and not prediction.startswith("Error:"):
                messages.success(request, f"Successfully predicted Job Role: {prediction}")
                # Save to history (keep existing logic)
                if request.user.is_authenticated:
                    try:
                        JobPredictionRecord.objects.create(user=request.user, input_features=job_input_data, predicted_role=prediction)
                        print(f"Saved job prediction record for user {request.user.username}")
                        messages.info(request, "Prediction saved to your history.")
                    except Exception as e:
                        print(f"ERROR saving job prediction record: {e}")
                        messages.warning(request, "Prediction made, but failed to save to history.")
                # Prepare context *with* result to show result page
                context = {'job_prediction_result': prediction}
                # Render result template variant (or use conditional logic in predict_job.html)
                # We are using conditional logic in the template, so just render the same template
                return render(request, 'predictor/predict_job.html', context)
            else:
                messages.error(request, f"Prediction failed. {prediction or 'An internal error occurred.'}")
                # Form is valid, but prediction failed - show form again with error
                # We need to pass the form back in the context
        else:
            # Form is invalid, errors will be in form.errors
            print("Job form is invalid:", form.errors.as_json())
            messages.error(request, "Please correct the errors highlighted below.")
            # Fall through to render the form again with errors

    # --- GET Request or Invalid POST ---
    if form is None: # If it's a GET request, instantiate an unbound form
        form = JobPredictionForm(features=feature_names_job, categories=ordinal_categories_job)

    # Context for rendering the form page (GET or invalid POST)
    context = {
        'form': form,
        'job_prediction_result': None, # Ensure result is None when showing form
        # No longer need to pass features/categories separately if form handles labels
    }
    return render(request, 'predictor/predict_job.html', context)

# predictor/views.py

@login_required
def predict_degree_view(request):
    """Handles the Degree Suggestion page and form submission using Django Forms."""
    if not feature_names_degree:
        messages.error(request, "Degree suggestion resources are not available.")
        return redirect('predictor:dashboard')

    form = None # Initialize form variable

    if request.method == 'POST':
        # Instantiate form with POST data AND dynamic fields
        form = DegreePredictionForm(request.POST, features=feature_names_degree)

        if form.is_valid():
            print("Degree form is valid. Processing prediction...")
            # Reconstruct input dict for the prediction function
            # form.cleaned_data will have {feature_name: True/False}
            degree_input_data = {
                feature: 1 for feature, selected in form.cleaned_data.items() if selected
            }
            prediction = predict_degree(degree_input_data) # Call helper

            # Handle prediction result (keep message logic)
            if prediction and not prediction.startswith("Error:"):
                messages.success(request, f"Successfully predicted Degree: {prediction}")
                # Save to history (keep existing logic)
                if request.user.is_authenticated:
                    try:
                        DegreePredictionRecord.objects.create(user=request.user, input_features=degree_input_data, predicted_degree=prediction)
                        print(f"Saved degree prediction record for user {request.user.username}")
                        messages.info(request, "Prediction saved to your history.")
                    except Exception as e:
                        print(f"ERROR saving degree prediction record: {e}")
                        messages.warning(request, "Prediction made, but failed to save to history.")
                # Prepare context *with* result
                context = {'degree_prediction_result': prediction}
                return render(request, 'predictor/predict_degree.html', context) # Show result page
            else:
                messages.error(request, f"Prediction failed. {prediction or 'An internal error occurred.'}")
                # Form valid, prediction failed - show form again
        else:
            # Form is invalid
            print("Degree form is invalid:", form.errors.as_json())
            messages.error(request, "An error occurred with your selections.") # Generic error
            # Fall through to render form with errors

    # --- GET Request or Invalid POST ---
    if form is None: # If GET, instantiate unbound form
        form = DegreePredictionForm(features=feature_names_degree)

    # Context for rendering the form page
    context = {
        'form': form,
        'degree_prediction_result': None,
        # No longer need to pass degree_features separately
    }
    return render(request, 'predictor/predict_degree.html', context)


def register(request):
    """ Handles user registration using the custom form. """
    if request.method == 'POST':
        # Use the custom form
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # Saves user with username, password, AND email
            login(request, user)
            messages.success(request, 'Registration successful! You are now logged in.')
            return redirect('predictor:index')
        else:
            messages.error(request, 'Please correct the registration errors below.')
    else: # GET request
        # Use the custom form
        form = CustomUserCreationForm()

    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required
def prediction_history(request):
    """Displays the paginated prediction history for the logged-in user."""

    # Fetch all records first, ordered as before
    job_history_list = JobPredictionRecord.objects.filter(user=request.user).order_by('-timestamp')
    degree_history_list = DegreePredictionRecord.objects.filter(user=request.user).order_by('-timestamp')

    # --- Pagination ---
    items_per_page = 10 # Show 10 records per page (adjust as needed)

    # Paginate Job History
    job_paginator = Paginator(job_history_list, items_per_page)
    job_page_number = request.GET.get('job_page') # Get page number from URL (?job_page=...)
    try:
        job_page_obj = job_paginator.page(job_page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        job_page_obj = job_paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        job_page_obj = job_paginator.page(job_paginator.num_pages)

    # Paginate Degree History
    degree_paginator = Paginator(degree_history_list, items_per_page)
    degree_page_number = request.GET.get('degree_page') # Get page number from URL (?degree_page=...)
    try:
        degree_page_obj = degree_paginator.page(degree_page_number)
    except PageNotAnInteger:
        degree_page_obj = degree_paginator.page(1)
    except EmptyPage:
        degree_page_obj = degree_paginator.page(degree_paginator.num_pages)

    context = {
        # Pass the Page objects to the template instead of the full lists
        'job_page_obj': job_page_obj,
        'degree_page_obj': degree_page_obj,
    }
    return render(request, 'predictor/history.html', context)


@login_required
def profile_view(request):
    """Displays user profile and handles updates."""
    # Profile is automatically created by signal, so it should exist
    # Use get_object_or_404 or try/except if you want to be extra safe
    profile = request.user.profile # Access profile via related_name

    if request.method == 'POST':
        # Pass instance=profile to update the existing profile
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save() # Save the updated profile data
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('predictor:profile') # Redirect back to profile page
        else:
            messages.error(request, 'Please correct the errors below.')
    else: # GET request
        # Populate form with current profile data
        form = ProfileUpdateForm(instance=profile)

    context = {
        'form': form,
        'profile': profile # Pass profile object for display
    }
    return render(request, 'predictor/profile.html', context)