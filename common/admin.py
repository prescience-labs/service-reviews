from django.contrib import admin

from common.models import Review

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('sentiment_analysis',)
admin.site.register(Review, ReviewAdmin)
