from django.db import models
from django.utils import timezone

from core.models import User

class BaseModel(models.Model):
    created = models.DateTimeField(verbose_name="Дата создания")
    updated = models.DateTimeField(verbose_name="Дата последнего обновления")

    class Meta:
        abstract = True

class GoalCategory(BaseModel):
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title

class Goal(BaseModel):
    class Status(models.IntegerChoices):
        todo = 1, 'toDO'
        in_progress = 2, 'in progress'
        done = 3, 'done'
        archived = 4, 'arhived'

    class Priority(models.IntegerChoices):
        low = 1, "L"
        medium = 2, 'M'
        high = 3,'H'
        critical = 4,'C'

    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(to=GoalCategory, on_delete=models.RESTRICT, related_name='goals')
    status = models.PositiveSmallIntegerField(choices=Status.choices,default=Status.todo)
    priory = models.PositiveSmallIntegerField(choices=Priority.choices, default=Priority.low)
    due_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='goals')


    class Meta:
        verbose_name = "Цель"
        verbose_name_plural = "Цель"

    def __str__(self):
        return self.title

class GoalComment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='comments')
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарий"