from __future__ import absolute_import, unicode_literals
from django_tgbot.state_manager import update_types
from fiuls_bot import bot_token
from fiuls_bot.bot import TelegramBot, state_manager
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.keyboardbutton import KeyboardButton
from django_tgbot.types.replykeyboardremove import ReplyKeyboardRemove
from fiuls_bot.models import TelegramChat
from django_tgbot.decorators import processor
from celery import shared_task
from datetime import datetime
import requests
import json

@shared_task(name = "send_message")
def send_message(text, bot_message, *args, **kwargs):
  bot = TelegramBot(bot_token, state_manager)

  if bot_message:
    url='https://shrimp-touched-mollusk.ngrok-free.app/text_generator/invoke'
    data = {"input": {"context":text}}
    response = requests.post(url, json = data, headers={"Content-Type":"application/json"})
    content_=json.loads(response.text)['output']
    try:
        content=json.loads(content_)['generated']
    except:
        content_=content_+'}'
        content=json.loads(content_)['generated']

  else:
    content=text
  
  chats=TelegramChat.objects.all()
  for chat in chats:
    chat_id=chat.telegram_id
    state=chat.telegram_states.all()[0]
    state.reset_memory()
    state.set_name('asked_response')
    bot.sendMessage(chat_id, content)
    bot.sendMessage(chat_id, '¿Ha realizado los ejercicios?')
