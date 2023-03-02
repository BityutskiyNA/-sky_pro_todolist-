from django.db import transaction
from django.shortcuts import render

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from .models import GoalCategory, Goal
from .permissions import IsOwnerOrReadOnly
from .serializers import GoalCreateSerializer, GoalCategorySerializer


class GoalCategoryCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer



class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(
            user_id=self.request.user.id,
            is_deleted=False
        )


class  GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(
            user_id=self.request.user.id,
            is_deleted=False
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_delete = True
            instance.save(update_fields=('is_deleted',))
            instance.goal.update(status=Goal.Status.archived)
        return instance
