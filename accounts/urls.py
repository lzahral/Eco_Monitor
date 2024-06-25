from django.urls import path
from . import views

urlpatterns = [
    # path('set-theme',views.theme ,name='theme'),
    # path('message',views.message,name='message'),
    # path('new-message',views.new_message,name='new-message'),
    path('register',views.Register.as_view(),name='register'),
    # path('read-message',views.read_message,name='read-message'),
    # path('edit-profile',views.EditProfile.as_view(),name='edit-profile'),
    # path('read-notification',views.read_notification,name='read-notification'),
    # path('delete-notification',views.delete_notification,name='delete-notification'),
    # path('read-all-notification',views.read_all_notification,name='read-all-notification'),
    path("edit-profile", views.EditProfile.as_view(), name="edit-profile"),
]
