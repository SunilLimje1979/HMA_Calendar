from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('demo/',views.demo,name='demo'),
    path('login/',views.login,name='login'),
    path('signup/',views.signup,name='signup'),
    path('logout/' , views.logout_view , name='logout'),
    path('get-events/', views.get_events_for_date, name='get_events'),
    path('add-event/', views.add_event_view, name='add_event'),
    path('update-event/<int:event_id>/', views.update_event_view, name='update_event'),
    path('remove-event/<int:event_id>/', views.remove_event_view, name='remove_event'),
    path('my_events_list/',views.my_events_list_view,name='my_events_list'),
]
