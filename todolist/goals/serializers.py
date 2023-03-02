from rest_framework import serializers, exceptions
from .models import GoalCategory, Goal

from core.serializers import UserUpdateSerialiser


class GoalCreateSerializer(serializers.ModelSerializer):
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
    # category = serializers.PrimaryKeyRelatedField(
    #     queryset=GoalCategorySerializer.objects.filter(is_deleted=True)
    # )
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ('id','create','updated', 'user')

    def validate_category(self, value):
        if self.context['request'].user != value.user:
            raise exceptions.PermissionDenied
        return value

