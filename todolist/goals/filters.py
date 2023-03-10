import django_filters
from django.db import models
from django_filters import rest_framework

from .models import Goal, GoalComment


class GoalDateFilter(rest_framework.FilterSet):
    class Meta:
        model = Goal
        fields = {
            "due_date": ("lte", "gte"),
            "category": ("exact", "in"),
            "status": ("exact", "in"),
            # "priority": ("exact", "in"),
        }

    filter_overrides = {
        models.DateField: {"filter_class": django_filters.IsoDateTimeFilter},
    }


class CommentFilter(django_filters.rest_framework.FilterSet):
    # goal__id = django_filters.NumberFilter()

    class Meta:
        model = GoalComment
        fields = {
            "goal": ("exact",),
        }

    filter_overrides = {
        models.SlugField: {"filter_class": django_filters.NumberFilter},
    }
