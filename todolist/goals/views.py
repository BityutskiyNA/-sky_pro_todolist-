from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from .filters import GoalDateFilter
from .models import GoalCategory, Goal, GoalComment
from .permissions import IsOwnerOrReadOnly
from .serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer, \
    CommentCreateSerializer, CommentSerializer


class GoalCategoryCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer



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
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goals.update(status=Goal.Status.archived)
        return instance

class GoalCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ['title','description']
    ordering =['title']
    searh_fields = ['title','description']

    def get_queryset(self):
        return Goal.objects.filter(
            Q(user_id=self.request.user.id) & ~Q(status=Goal.Status.archived) & Q(category__is_deleted=False)
        )


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    permission_classes =  [permissions.IsAuthenticated]
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.filter(
            Q(user_id=self.request.user.id) & ~Q(status=Goal.Status.archived) & Q(category__is_deleted=False)
        )

class CommentCreateView(CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CommentCreateSerializer


class CommentListView(ListAPIView):
        model = GoalComment
        permission_classes = [permissions.IsAuthenticated]
        serializer_class = CommentSerializer
        filter_backends = [
            DjangoFilterBackend,
            filters.OrderingFilter,
            filters.SearchFilter,
        ]
        # filterset_class = GoalDateFilter
        ordering_fields = ['created']
        ordering = ['created']
        searh_fields = ['goal']

        def get_queryset(self):
            return GoalComment.objects.filter(user_id=self.request.user.id)


class CommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    permission_classes =  [permissions.IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return GoalComment.objects.filter(user_id=self.request.user.id)
