from django.db import migrations, transaction
from django.utils import timezone

def create_objects(apps, schema_editor):

    User = apps.get_model("core", "User")
    Board = apps.get_model("goals", "Board")
    BoardParticipant = apps.get_model("goals", "BoardParticipant")
    GoalCategory = apps.get_model("goals", "GoalCategory")

    now = timezone.now()

    with transaction.atomic():  # Применяем все изменения одной транзакцией
        for user_id in User.objects.values_list('id',flat=True):  # Для каждого пользователя
            new_board = Board.objects.create(
                title="Мои цели",
                created=now,  # Проставляем вручную по той же причине, что описана вверху
                updated=now
            )
            BoardParticipant.objects.create(
                user_id=user_id,
                board=new_board,
                role=1,  # Владелец, проставляем числом, не импортируем код по той же причине
                created=now,
                updated=now
            )

            # проставляем всем категориям пользователя его доску
            GoalCategory.objects.filter(user_id=user_id).update(board=new_board)


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0003_board_alter_goal_created_alter_goal_updated_and_more'),
    ]

    operations = [
        migrations.RunPython(create_objects)
    ]
