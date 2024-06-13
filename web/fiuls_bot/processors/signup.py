from django_tgbot.decorators import processor
from django_tgbot.state_manager import message_types, update_types, state_types
from django_tgbot.types.update import Update
from django_tgbot.exceptions import ProcessFailure
from django_tgbot.types.replykeyboardmarkup import ReplyKeyboardMarkup
from django_tgbot.types.replykeyboardremove import ReplyKeyboardRemove
from django_tgbot.types.keyboardbutton import KeyboardButton
from ..bot import state_manager, TelegramBot
from ..models import TelegramState
import requests
import json 

state_manager.set_default_update_types(update_types.Message)


@processor(state_manager, from_states='asked_response', fail=state_types.Keep, message_types=message_types.Text)
def get_response(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    text = update.get_message().get_text()

    url='https://shrimp-touched-mollusk.ngrok-free.app/text_analysis/invoke'
    data = {'input': {'user_response': text}}
    response = requests.post(url, json = data, headers={"Content-Type":"application/json"})
    content_=json.loads(response.text)['output']
    try:
        r=json.loads(content_)
    except:
        content_=content_+'}'
        r=json.loads(content_)
        pass
    if r['value'] >= 0.5:
        context = 'Genera un texto de refuerzo positivo para un usario que ha realizado ejercicios durante la semana.'
        state.set_name('question')
    else:
        #identificar barrera
        context = 'Generao un texto preguntando a un usuario porque no ha realizado sus ejercicios'
        state.set_name('deliver_facilitator')

    state.set_memory({
    'text': text
    })

    url='https://shrimp-touched-mollusk.ngrok-free.app/text_generator/invoke'
    data = {"input": {"context":context}}
    response = requests.post(url, json = data, headers={"Content-Type":"application/json"})
    content_=json.loads(response.text)['output']
    try:
        content=json.loads(content_)['generated']
    except:
        content_=content_+'}'
        content=json.loads(content_)['generated']
        pass

    bot.sendMessage(chat_id, content, reply_markup=ReplyKeyboardRemove.a(remove_keyboard=True))

@processor(state_manager, from_states='deliver_facilitator', success=state_types.Reset, fail=state_types.Keep, message_types=message_types.Text)
def deliver_facilitator(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    text = update.get_message().get_text()
    
    context = 'Genera una respuesta para ayudar al usuario respecto a la razon de la cual no ha realizado sus ejercicios. la rason es la siguiente:'+text
    state.set_name('question')
       
    state.set_memory({
    'text': text
    })

    url='https://shrimp-touched-mollusk.ngrok-free.app/text_generator/invoke'
    data = {"input": {"context":context}}
    response = requests.post(url, json = data, headers={"Content-Type":"application/json"})
    content_=json.loads(response.text)['output']
    try:
        content=json.loads(content_)['generated']
    except:
        content_=content_+'}'
        content=json.loads(content_)['generated']
        pass

    bot.sendMessage(chat_id, content, reply_markup=ReplyKeyboardRemove.a(remove_keyboard=True))

@processor(state_manager, from_states='question', success=state_types.Keep, fail=state_types.Keep, message_types=message_types.Text)
def get_question(bot: TelegramBot, update: Update, state: TelegramState):
    chat_id = update.get_chat().get_id()
    question = update.get_message().get_text()
    if len(question) < 3:
        bot.sendMessage(chat_id, 'La pregunta es muy corta, intente nuevamente')
        raise ProcessFailure

    state.set_memory({
        'text': question
    })

    state.set_name('question')

    url='https://shrimp-touched-mollusk.ngrok-free.app/bot/invoke'
    data = {"input": {"question": question, "generation":"","documents":[]}}
    response = requests.post(url, json = data, headers={"Content-Type":"application/json"})
    content=json.loads(response.text)['output']['generation']

    bot.sendMessage(chat_id, content)