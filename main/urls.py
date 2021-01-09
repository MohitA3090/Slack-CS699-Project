from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('<slug:workspace>/<slug:channel>/', views.home1, name='home1'),
    path('<slug:workspace>/<slug:channel>/add-user-ws/', views.add_user_to_workspace, name='add_user_to_workspace'),
    path('<slug:workspace>/<slug:channel>/add-user-ch/', views.add_user_to_channel, name='add_user_to_channel'),
    path('<slug:workspace>/<slug:channel>/add-channel/', views.add_channel_to_workspace, name='add_channel_to_workspace'),
    path('create-worskspace/', views.create_workspace, name='create_workspace'),
    path('showreply/', views.show_reply, name = 'showreply'),
    path('reset/', views.change_password, name = 'change_password'),
    path('logout/', views.logout, name = 'logout')
]
