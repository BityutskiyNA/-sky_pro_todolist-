import logging
import os
import sys

import redis
from django.conf import settings
from django.core.management import BaseCommand
from typing import Optional

sys.path.append("D:\\python_pr\\sky_pro_f_pr\\todolist\\")
from bot.models import TgUser
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory
from bot.tg.client import TgClient
from settings_pd import Settings_TDL


setings_bs = Settings_TDL()

class Command(BaseCommand):

    def __init__(self):
        super().__init__()
        self.tg_client = TgClient(token=settings.BOT_TOKEN)
        self.__tg_user: Optional[TgUser] = None
        self.logger = logging.getLogger(__name__)
        self.redis_cache = self._get_cache()
        self.logger.info('Bot start pooling')

    @property
    def tg_user(self):
        if self.__tg_user:
            return self.__tg_user
        raise RuntimeError('User not exist')


    @staticmethod
    def _get_verification_code()->str:
        return os.urandom(12).hex()

    def handle(self, *args, **options):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1

                self.__tg_user, _ = TgUser.objects.get_or_create(
                    chat_id=item.message.chat.id,
                    defaults={'username':item.message.from_.username}
                )
                if self.__tg_user.user_id:
                    self._handle_verifed_user(item.message)
                else:
                    self._handle_unver_user(item.message)

    def _handle_unver_user(self, message: Message):
        self.tg_user.verification_code = self._get_verification_code()
        self.tg_user.save(update_fields=('verification_code',))

        self.tg_client.send_message(
            chat_id=message.chat.id,
            text=f'verification code {self.tg_user.verification_code}'
        )

    def _handle_verifed_user(self, message: Message):
        if message.text.startswith('/'):
            self._hadle_command(message)
        else:
            self._hadle_message(message)


    def _hadle_command(self, message: Message):
        if isinstance(message.text, str) and message.text == '/goals':
            self._handle_goal_command(message)
        elif isinstance(message.text, str) and message.text == '/create':
            self._handle_goal_create_command(message)
        elif isinstance(message.text, str) and message.text == '/cancel':
            self._handle_cancel_command(message)
        else:
            raise NotImplementedError


    def _hadle_message(self, message: Message):
        goal_state = self.redis_cache.lrange(self.__tg_user.user_id, 0, -1)

        if len(goal_state) == 1:
            category = GoalCategory.objects.filter(user_id=self.tg_user.user_id, title=message.text)
            if len(category) == 0:
                self.tg_client.send_message(chat_id=message.chat.id,
                    text='Категория с таким названием не найдена, введите корректную категорию')
            else:
                self.redis_cache.rpush(self.__tg_user.user_id, message.text)
                self.tg_client.send_message(chat_id=message.chat.id,text='Укажите название цели')
        elif len(goal_state) == 2:
            category_title = goal_state[1]
            category = GoalCategory.objects.filter(user_id=self.tg_user.user_id, title=category_title)
            if len(category) != 0:
                goal_list = {
                        'category':category[0],
                        'title': message.text,
                    }
                self._create_goal(goal_list)
                self.tg_client.send_message(chat_id=message.chat.id,text='Задание создано')
                self.redis_cache.delete(self.__tg_user.user_id)

    def _handle_goal_command(self,message: Message):
        goals =list(
            Goal.objects.filter(user_id=self.tg_user.user_id)
            .exclude(status=Goal.Status.archived)
            .values_list('title', flat=True)
            )
        if goals:
            self.tg_client.send_message(
                chat_id=message.chat.id,
                text='\n'.join(goals)
            )
        else:
            self.tg_client.send_message(
                chat_id=message.chat.id,
                text="У вас нет целей"
            )

    def _get_cache(self):
        r = redis.StrictRedis(
            host=setings_bs.REDIS_HOST,
            port=setings_bs.REDIS_PORT,
            password=setings_bs.REDIS_PASSWORD,
            charset = "utf-8",
            decode_responses=True,
        )
        return r

    def _handle_goal_create_command(self, message: Message):
        self.redis_cache.delete(self.__tg_user.user_id)
        self.redis_cache.rpush(self.__tg_user.user_id,'goal_create')
        self.tg_client.send_message(
            chat_id=message.chat.id,
            text='Укажите категорию для цели'
        )
        goals_category = list(
            GoalCategory.objects.filter(user_id=self.tg_user.user_id).values_list('title', flat=True)
            )
        self.tg_client.send_message(
            chat_id=message.chat.id,
            text='\n'.join(goals_category)
        )

    def _handle_cancel_command(self, message: Message):
        self.redis_cache.delete(self.__tg_user.user_id)
        self.tg_client.send_message(
            chat_id=message.chat.id,
            text='Создание цели отменено'
        )

    def _create_goal(self, goal_list):
         Goal.objects.create(
            title=goal_list['title'],
            category=goal_list['category'],
            description=goal_list['title'],
            user= self.tg_user.user,
        )