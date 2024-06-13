from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.keyboardbutton import KeyboardButton
from django_tgbot.types.replykeyboardremove import ReplyKeyboardRemove
from ..bot import state_manager, TelegramBot
from ..models import TelegramState


state_manager.set_default_update_types(update_types.Message)


@processor(state_manager, success='question')
def say_hello(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    bot.sendMessage(chat_id, 'Hola, bienvenido al chat del proyecto FIULS Inicia')
    bot.sendMessage(chat_id, 'Este asistente te recordará diariamente a hacer tus ejercicios y te apoyará en tu proceso de recuperación. Puedes hacerle cualquier consulta en relación a la artrosis de rodilla.')

