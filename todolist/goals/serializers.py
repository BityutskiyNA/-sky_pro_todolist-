from django.db.models import Q
from rest_framework import serializers, exceptions
from .models import GoalCategory, Goal, GoalComment

from core.serializers import UserUpdateSerialiser


class GoalCategoryCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'is_geleted')


class GoalCategorySerializer(serializers.ModelSerializer):
    user = UserUpdateSerialiser(read_only=True)

    class Meta:
        model = GoalCategory
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user', 'is_geleted')


class GoalCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=GoalCategory.objects.filter(is_deleted=False)
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id','create','updated', 'user')

    def validate_category(self, value):
        if self.context['request'].user != value.user:
            raise exceptions.PermissionDenied
        return value

class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id', 'created', 'updated', 'user')


class CommentCreateSerializer(serializers.ModelSerializer):
    goal = serializers.PrimaryKeyRelatedField(
        queryset=Goal.objects.filter(status=Goal.Status.archived)
    )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id','create','updated', 'text','goal')

    def validate_category(self, value):
        if self.context['request'].user != value.user:
            raise exceptions.PermissionDenied
        return value


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoalComment
        fields = '__all__'
        read_only_fields = ('id','create','updated', 'text','goal')