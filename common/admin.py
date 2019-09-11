from django.contrib import admin

from common.models import Review

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('sentiment_analysis', 'created_at', 'updated_at',)
admin.site.register(Review, ReviewAdmin)
