import factory.django
from django.utils import timezone

from pytest_factoryboy import register

from core.models import User
from goals.models import Board, GoalCategory, BoardParticipant, Goal, GoalComment


@register
class UserFactory(factory.django.DjangoModelFactory):
    username = 'test_user'
    password = 'test_password_1'
    is_active = True
    email = 'test@test.ru'

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._get_manager(model_class).create_user(*args, **kwargs)


class DatesFactoryMixin(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True

    created = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)


@register
class BoardFactory(DatesFactoryMixin):
    title = 'test_board'

    class Meta:
        model = Board

    @factory.post_generation
    def with_owner(self, create, owner, **kwargs):
        if owner:
            BoardParticipant.objects.create(board=self, user=owner, role=BoardParticipant.Role.owner)


@register
class BoardParticipantFactory(DatesFactoryMixin):
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = BoardParticipant


@register
class GoalCategoryFactory(DatesFactoryMixin):
    title = 'test_goal_category'
    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)

    class Meta:
        model = GoalCategory


@register
class GoalFactory(DatesFactoryMixin):
    title = 'test_goal'
    category = factory.SubFactory(GoalCategoryFactory)

    class Meta:
        model = Goal


@register
class GoalCommentFactory(DatesFactoryMixin):
    user = factory.SubFactory(UserFactory)
    goal = factory.SubFactory(GoalCategoryFactory)
    text = 'test_goal_kommit'

    class Meta:
        model = GoalComment
