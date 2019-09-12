from django.contrib import admin

from common.models import Review, ReviewRequest

class ReviewAdmin(admin.ModelAdmin):
    readonly_fields = ('sentiment_analysis', 'created_at', 'updated_at',)
admin.site.register(Review, ReviewAdmin)

class ReviewRequestAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at',)
admin.site.register(ReviewRequest, ReviewRequestAdmin)
