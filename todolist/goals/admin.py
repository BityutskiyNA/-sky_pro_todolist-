from django.contrib import admin

from .models import GoalCategory, Goal, GoalComment


admin.site.register(GoalCategory)
admin.site.register(Goal)
admin.site.register(GoalComment)
