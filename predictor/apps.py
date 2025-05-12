from django.apps import AppConfig


class PredictorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'predictor'

    # Add this method to import signals when the app is ready
    def ready(self):
        import predictor.models # Import models where signals are defined
