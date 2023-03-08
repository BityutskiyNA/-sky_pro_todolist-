from django.db import transaction
from django.db.models import Q
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters
from rest_framework.pagination import LimitOffsetPagination

from .filters import GoalDateFilter
from .models import GoalCategory, Goal, GoalComment, Board
from .permissions import IsOwnerOrReadOnly, BoardPermissions, GoalCategoryPermissions, GoalPermissions, \
    CommentPermissions
from .serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer, \
    CommentCreateSerializer, CommentSerializer, BoardSerializer, BoardCreateSerializer


# @method_decorator(ensure_csrf_cookie, name='dispatch')
class GoalCategoryCreateView(CreateAPIView):
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategoryCreateSerializer


# @method_decorator(ensure_csrf_cookie, name='dispatch')
class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategorySerializer
    filterset_fields= ['board']
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        # return GoalCategory.objects.select_related('user').filter(
        return GoalCategory.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id,
            # user_id=self.request.user.id,
            is_deleted=False
        )

# @method_decorator(ensure_csrf_cookie, name='dispatch')
class  GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    # def get_queryset(self):
    #     return GoalCategory.objects.select_related('user').filter(
    #         user_id=self.request.user.id,
    #         is_deleted=False
    #     )

    def get_queryset(self):
        # return GoalCategory.objects.select_related('user').filter(
        return GoalCategory.objects.prefetch_related('board__participants').filter(
            board__participants__user_id=self.request.user.id,
            # user_id=self.request.user.id,
            is_deleted=False
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted',))
            instance.goals.update(status=Goal.Status.archived)
        return instance

# @method_decorator(ensure_csrf_cookie, name='dispatch')
class GoalCreateView(CreateAPIView):
    permission_classes = [GoalPermissions]
    serializer_class = GoalCreateSerializer

# @method_decorator(ensure_csrf_cookie, name='dispatch')
class GoalListView(ListAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
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
            Q(category__board__participants__user_id=self.request.user.id)
            & ~Q(status=Goal.Status.archived)
            & Q(category__is_deleted=False)
        )

# @method_decorator(ensure_csrf_cookie, name='dispatch')
class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.filter(
            Q(user_id=self.request.user.id) & ~Q(status=Goal.Status.archived) & Q(category__is_deleted=False)
        )
# @method_decorator(ensure_csrf_cookie, name='dispatch')
class CommentCreateView(CreateAPIView):
    permission_classes = [CommentPermissions]
    serializer_class = CommentCreateSerializer

# @method_decorator(ensure_csrf_cookie, name='dispatch')
class CommentListView(ListAPIView):
        model = GoalComment
        permission_classes = [CommentPermissions]
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
            return GoalComment.objects.filter(
                # user_id=self.request.user.id,
                category__board__participants__user_id=self.request.user.id

            )

# @method_decorator(ensure_csrf_cookie, name='dispatch')
class CommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    permission_classes = [CommentPermissions]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return GoalComment.objects.filter(user_id=self.request.user.id)

# @method_decorator(ensure_csrf_cookie, name='dispatch')
class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        return Board.objects.prefetch_related('participants').filter(
            participants__user_id=self.request.user.id,
            is_deleted=False
        )

    def perform_destroy(self, instance: Board):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=('is_deleted'))
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance

# @method_decorator(ensure_csrf_cookie, name='dispatch')
class BoardCreateView(CreateAPIView):
    permission_classes = [BoardPermissions]
    serializer_class = BoardCreateSerializer

# @method_decorator(ensure_csrf_cookie, name='dispatch')
class BoardListView(ListAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardCreateSerializer
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return Board.objects.prefetch_related('participants').filter(
            participants__user_id=self.request.user.id,
            is_deleted=False
        )