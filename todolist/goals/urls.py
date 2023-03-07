
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [
    path("board/create",  csrf_exempt(views.BoardCreateView.as_view())),
    path("board/list",  csrf_exempt(views.BoardListView.as_view())),
    path("board/<pk>",  csrf_exempt(views.BoardView.as_view())),

    path("goal_category/create",  csrf_exempt(views.GoalCategoryCreateView.as_view())),
    path("goal_category/list",  csrf_exempt(views.GoalCategoryListView.as_view())),
    path("goal_category/<pk>",  csrf_exempt(views.GoalCategoryView.as_view())),

    path("goal/create",  csrf_exempt(views.GoalCreateView.as_view())),
    path("goal/list",  csrf_exempt(views.GoalListView.as_view())),
    path("goal/<pk>",  csrf_exempt(views.GoalView.as_view())),

    path("goal_comment/create",  csrf_exempt(views.CommentCreateView.as_view())),
    path("goal_comment/list",  csrf_exempt(views.CommentListView.as_view())),
    path("goal_comment/<pk>",  csrf_exempt(views.CommentView.as_view())),
]