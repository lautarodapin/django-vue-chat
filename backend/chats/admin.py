from django.contrib import admin

from .models import Message, Chat


class MessageInline(admin.TabularInline):
    model = Message


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    inlines = [MessageInline]

