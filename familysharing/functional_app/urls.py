from django.urls import path
from functional_app.views import *
from authorization_app import views as authapp_views
from FS_chat import views as chat_views
from django.contrib.auth import views as authViews
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', authapp_views.check_session),
    path('home/', first_page),
    path('id=<page_id>', users_page),
    path('exit/', authViews.LogoutView.as_view(next_page='/'), name='exit'),
    path('redirect', redirect_on_personal_page, name='my_page'),
    path('search/', search_page, name='search_page'),
    path('messages/', chat_views.chat_list, name='chat_list'),
    path('create_chat=<page_id>', chat_views.create_chat),
    path('chat_id=<chat_id>', chat_views.chat)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

