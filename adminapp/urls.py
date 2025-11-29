from django.urls import path
from . import views

urlpatterns = [
    path('', views.adminlogin, name='adminlogin'),
    path('adminBase/',views.adminBase,name='adminBase'),
    path('adminIndex/',views.adminIndex,name='adminIndex'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('registeredmembers/',views.registeredmembers,name='registeredmembers'),
    path('all_events/',views.all_events,name='all_events'),
    path('all-events/', views.all_events, name='all_events'),
    path('save-event/', views.save_event_ajax, name='save_event_ajax'),
    path('get-event-details/', views.get_event_details, name='get_event_details'),
    path('search-users/', views.search_users_ajax, name='search_users_ajax'),
    path('delete-event/', views.delete_event_ajax, name='delete_event_ajax'), 
]
