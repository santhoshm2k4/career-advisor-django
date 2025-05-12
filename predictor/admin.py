# predictor/admin.py
from django.contrib import admin
from .models import JobPredictionRecord, DegreePredictionRecord

@admin.register(JobPredictionRecord)
class JobPredictionRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'predicted_role', 'timestamp')
    list_filter = ('user', 'timestamp', 'predicted_role')
    search_fields = ('user__username', 'predicted_role')
    readonly_fields = ('user', 'timestamp', 'input_features', 'predicted_role') # Make fields read-only in admin

@admin.register(DegreePredictionRecord)
class DegreePredictionRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'predicted_degree', 'timestamp')
    list_filter = ('user', 'timestamp', 'predicted_degree')
    search_fields = ('user__username', 'predicted_degree')
    readonly_fields = ('user', 'timestamp', 'input_features', 'predicted_degree')