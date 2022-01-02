from rest_framework.routers import DefaultRouter
from . import views

router  = DefaultRouter()
router.register('chats', views.ChatViewSet, basename='chat')
router.register('messages', views.MessageViewSet, basename='message')

urlpatterns = router.urls
