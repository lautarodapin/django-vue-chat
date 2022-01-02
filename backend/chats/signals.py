from typing import Any, Dict, Literal, Set
from django.dispatch import receiver
from django.db.models.signals import post_save, m2m_changed
from .models import Chat, Message
from users.models import User
from core.models import TimestampedModel

# @receiver(m2m_changed, sender=Chat.active_users.through)
# def notify_user_joined(
#     sender,
#     instance: Chat,
#     action: Literal['pre_add', 'post_add', 'pre_remove', 'post_remove'],
#     reverse: bool,
#     pk_set: Set[int],
#     **kwargs: Dict[str, Any],
# ):
#     if not pk_set: return
#     user = User.objects.get(pk=pk_set.pop())
#     if not reverse and action == 'post_add':
#         Message.objects.create(
#             text=f'User "{user}" joined the chat.',
#             chat=instance,
#         )
#     if not reverse and action == 'post_remove':
#         Message.objects.create(
#             text=f'User "{user}" leave the chat.',
#             chat=instance,
#         )


@receiver(post_save)
def my_callback(sender, instance, **kwargs):
    if issubclass(sender, TimestampedModel):
        import inspect
        for frame_record in inspect.stack():
            if frame_record[3]=='get_response':
                request = frame_record[0].f_locals['request']
                break
        else:
            request = None
        if request and request.user and request.user.is_authenticated:
            if kwargs.get('created', None):
                sender.objects.filter(id=instance.id).update(
                    created_by=request.user,
                    mod_by=request.user,
                )
            else:
                sender.objects.filter(id=instance.id).update(
                    mod_by=request.user,
                )