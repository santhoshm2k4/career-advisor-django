# Career Advisor: AI-Powered Job & Degree Guidance

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [ML Model Details](#ml-model-details)
5. [Project Structure](#project-structure)
6. [Setup and Installation](#setup-and-installation)
7. [Usage](#usage)
8. [Challenges & Learnings](#challenges--learnings)
9. [Future Enhancements](#future-enhancements)
10. [Contributors](#contributors)
11. [License](#license) (Optional)

## Introduction

The Career Advisor is a full-stack web application designed to assist users in making informed decisions about potential job roles and academic degree programs. It leverages Machine Learning models to provide personalized, data-driven suggestions based on user-provided skills and interests. The goal is to simplify the often overwhelming process of career exploration.

## Features

*   **AI Job Role Prediction:** Suggests suitable job roles based on user input of proficiency levels across 17 key skills.
*   **AI Degree Suggestion:** Recommends relevant degree programs based on a selection from 59 diverse interests.
*   **User Authentication:** Secure system for:
    *   User Registration (with email)
    *   Login & Logout
    *   Password Reset functionality
*   **Personalized Dashboard:** A central hub for logged-in users to navigate the application's features.
*   **Prediction History:** Users can view a chronological and paginated history of their past job and degree predictions, including the inputs provided for each.
*   **User Profile Management:** Users can view their basic account information and update their full name.
*   **Interactive UI:** User-friendly interface with clickable cards for skill/interest selection, built with Bootstrap 5 for responsiveness.
*   **Django Messages Framework:** Provides feedback to users for actions like successful registration, predictions, or errors.

## Technology Stack

*   **Backend:** Python 3.11, Django 5.2
*   **Machine Learning:**
    *   Scikit-learn (for RandomForestClassifier, OrdinalEncoder, LabelEncoder)
    *   Pandas (for data manipulation)
    *   NumPy (for numerical operations)
    *   Joblib (for model persistence and loading)
*   **Frontend:**
    *   HTML5
    *   CSS3
    *   JavaScript (Vanilla JS for UI interactions)
    *   Bootstrap 5 (for responsive design and components)
    *   Font Awesome (for icons)
*   **Database:** SQLite 3 (for development)
*   **Version Control:** Git & GitHub
*   **Development Environment:** [e.g., VS Code, PyCharm, Standard Python Environment]

## ML Model Details

### Job Role Prediction Model
*   **Algorithm:** RandomForestClassifier (Scikit-learn)
*   **Dataset:** `dataset9000.csv` (approx. 9,000 samples)
*   **Features (17):** Skill proficiency levels (e.g., 'Database Fundamentals', 'Programming Skills')
    *   *Encoding:* OrdinalEncoder with categories: `['Not Interested', 'Poor', 'Beginner', 'Average', 'Intermediate', 'Excellent', 'Professional']`
*   **Target (17 Roles):** Job role categories (e.g., 'Database Administrator', 'Software Developer')
    *   *Encoding:* LabelEncoder

### Degree Suggestion Model
*   **Algorithm:** RandomForestClassifier (Scikit-learn)
*   **Dataset:** `stud.csv` (approx. 20,000 samples)
*   **Features (59):** User interests (e.g., 'Coding', 'Drawing', 'Sports')
    *   *Encoding:* Binary (1 if selected, 0 if not) - handled directly by model input.
*   **Target (35 Degrees):** Degree program names (e.g., 'B.Tech.-Computer Science and Engineering')
    *   *Encoding:* LabelEncoder

## Project Structure

```plaintext
career_advisor/
├── career_advisor/            # Django project configuration directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py            # Project settings
│   ├── urls.py                # Project-level URL routing
│   └── wsgi.py
├── ml_models/                 # Directory for saved ML models and artifacts
│   ├── ml_models_degree/
│   │   ├── rf_degree_model.joblib
│   │   └── … (other degree artifacts)
│   └── ml_models_job_9k/
│       ├── rf_model_job_9k.joblib
│       └── … (other job artifacts)
├── predictor/                 # Main Django application
│   ├── __init__.py
│   ├── admin.py               # Admin site configurations
│   ├── apps.py                # App configuration (signals imported here)
│   ├── forms.py               # Django forms for input and validation
│   ├── migrations/
│   ├── models.py              # Database models (User Profile, Prediction History)
│   ├── urls.py                # App-level URL routing
│   ├── views.py               # View logic, prediction handling
│   └── … (other app files)
├── templates/                 # Project-level templates
│   ├── predictor/             # Templates for the ‘predictor’ app (base, dashboard, etc.)
│   │   ├── base.html
│   │   └── … (other templates)
│   └── registration/          # Templates for authentication (login, register, etc.)
│       ├── login.html
│       └── … (other templates)
├── db.sqlite3                 # SQLite database file (should be in .gitignore)
├── manage.py                  # Django’s command-line utility
├── README.md                  # This file
├── requirements.txt           # Python package dependencies
└── .gitignore                 # Specifies intentionally untracked files
```


## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/santhoshm2k4/career-advisor-django.git
    cd career-advisor-django
    ```
2.  **Create and activate a virtual environment** (recommended):
    ```bash
    python -m venv venv
    # On Windows:
    venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: Ensure your `requirements.txt` file is up-to-date with all necessary packages: Django, scikit-learn, pandas, numpy, joblib)*
4.  **Place ML Model Artifacts:**
    Ensure the saved `.joblib` files for the ML models and encoders are placed in the correct subdirectories within the `ml_models/` folder as outlined in `predictor/views.py`. (Alternatively, provide instructions if they need to be generated or downloaded).
5.  **Apply database migrations:**
    ```bash
    python manage.py makemigrations predictor
    python manage.py migrate
    ```
6.  **Create a superuser** (for admin access and initial login):
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create an admin user.
7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
8.  Open your web browser and navigate to `http://127.0.0.1:8000/`.

## Usage

1.  **Register:** If you are a new user, click on "Register" and create an account.
2.  **Login:** Existing users can log in with their credentials.
3.  **Dashboard:** After logging in, you will be directed to the dashboard.
4.  **Predict Job Role:** Navigate to "Job Predictor", select your proficiency level for each skill, and click "Predict Job Role".
5.  **Predict Degree:** Navigate to "Degree Predictor", select your interests, and click "Predict Degree".
6.  **View History:** Click on "History" to see a list of your past predictions and the inputs used.
7.  **View/Edit Profile:** Access "My Profile" from the user dropdown to view your details and update your full name.
8.  **Logout:** Use the logout option from the user dropdown.

## Challenges & Learnings

*   **ML Model Integration:** Integrating pre-trained Scikit-learn models into a live Django application involved using `joblib` for persistence and carefully managing the loading of models and encoders at server startup.
*   **Data Preprocessing Consistency:** Ensuring that user input from web forms is preprocessed (e.g., using OrdinalEncoder) in exactly the same way as the training data was crucial for accurate predictions.
*   **Dynamic Form Generation:** Creating Django forms with fields determined at runtime (based on loaded feature lists) required customizing the form's `__init__` method.
*   **User Experience (UX):** Improving the input mechanism from standard dropdowns/checkboxes to more interactive clickable cards for skills and interests significantly enhanced usability.
*   **Django Signals:** Implementing automatic profile creation upon user registration using `post_save` signals, and handling cases for users created before the profile system was in place.
*   **Authentication Flow:** Managing Django's built-in authentication, including CSRF protection for logout and implementing custom registration forms.

## Future Enhancements

*   **Deployment:** Deploy the application to a cloud platform (e.g., PythonAnywhere, Heroku, AWS).
*   **Email Service Integration:** Configure a transactional email service (e.g., SendGrid) for password reset emails.
*   **Automated Testing:** Implement comprehensive unit and integration tests.
*   **Expanded User Profile:** Add more fields like bio, education, work experience.
*   **Advanced History Features:** Introduce filtering, sorting, and searching for prediction history.
*   **Model Iteration:** Explore different ML models, feature engineering, and potentially incorporate user feedback to refine predictions.
*   **Admin Interface Enhancements:** Customize the Django admin for better management of user data and prediction records.
*   **API Development:** Potentially expose prediction functionality via an API for other applications.
