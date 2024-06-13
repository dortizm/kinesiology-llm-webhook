from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('title','text','bot_message','human_readable')

admin.site.register(Message, MessageAdmin)