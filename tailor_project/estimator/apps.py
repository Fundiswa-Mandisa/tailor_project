from django.apps import AppConfig


class EstimatorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'estimator'

    def ready(self):
        """Load the ML model when Django starts."""
        import logging
        logger = logging.getLogger(__name__)
        try:
            from django.conf import settings
            from .ml.predictor import predictor
            predictor.load(
                model_path=str(settings.ML_MODEL_PATH),
                dataset_path=str(settings.ML_DATASET_PATH),
            )
            logger.info("✓ Tailor ML model loaded successfully.")
        except Exception as e:
            logger.warning("⚠ ML model load deferred: %s", e)
