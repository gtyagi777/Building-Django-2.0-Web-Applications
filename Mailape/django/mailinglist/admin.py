from django.contrib import admin
from mailinglist.models import MailingList, Subscriber, Message



admin.site.register(MailingList)
admin.site.register(Subscriber)
admin.site.register(Message)