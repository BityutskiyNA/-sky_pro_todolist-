from django.contrib import admin

from .models import GoalCategory, Goal, GoalComment

# class GoalCategoryAdmin(admin.ModelAdmin):
#     list_display = ("title", "user", "created", "updated")
#     search_fields = ("title", "user")

admin.site.register(GoalCategory)
admin.site.register(Goal)
admin.site.register(GoalComment)