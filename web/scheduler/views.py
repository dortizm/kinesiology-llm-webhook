from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST,require_GET
from django.http import HttpResponse
from .models import Message
import json
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from fiuls_bot.models import TelegramUser, TelegramChat
from .forms import ScheduleForm
from django_celery_beat.models import PeriodicTask,CrontabSchedule

def index(request):
    users=TelegramUser.objects.all().count()
    chats=TelegramChat.objects.all().count()
    return render(request, 'index.html', {'users':users,'chats':chats})

def scheduler(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            week_days=form.cleaned_data["week_days"]
            time=form.cleaned_data["time"]
            bot_message=form.cleaned_data["bot_message"]
            if week_days:
                week_days=', '.join(week_days)
                day='*'
                month='*'
            else:
                week_days='*'
                day=form.cleaned_data["day"]
                month=form.cleaned_data["month"]
            hour=time.hour
            minute=time.minute
            crontab=CrontabSchedule(minute=minute,hour=hour,day_of_week=week_days,day_of_month=day,month_of_year=month)
            crontab.save()
            task=PeriodicTask.objects.create(crontab=crontab,name=title,one_off=False,task='send_message',args='["'+text+'","'+str(bot_message)+'"]')
            schedule=Message(title=title,text=text,schedule=task,bot_message=bot_message)
            schedule.save()
            return redirect('index')
    else:
        form = ScheduleForm()
    return render(request, 'scheduler.html', {'form': form})
