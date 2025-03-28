from django.urls import path 
from . import views 


urlpatterns = [ 
    # User related URLs
    path('signup/manager/',  views.manager_signup,  name='manager_signup'),
    path('signup/operator/', views.operator_signup, name='operator_signup'),
    path('login',            views.user_login,      name='login'),
    path('logout/',          views.user_logout,     name='logout'),



    # Manager related URLs
    path('dashboard',                    views.manager_dashboard,  name='manager_dashboard'),
    path('create_queue',                 views.create_queue,       name='create_queue'),
    path('modify_queue/<int:queue_id>/', views.modify_queue,       name='modify_queue'),
    path('generate_qr/<int:queue_id>/',  views.generate_qr_code,   name='generate_qr_code'),
    path('modify_operator/<int:operator_pk>/', views.modify_operator,       name='modify_operator'),
   
    path('queue/<int:queue_id>/delete/',         views.delete_queue_confirm, name='delete_queue_confirm'),
    path('queue/<int:queue_id>/delete/confirm/', views.delete_queue,         name='delete_queue'),

    path('stats', views.queue_operator_stats_view,         name='queue_operator_stats_view'),
    
   
    path('operator_dashboard', views.operator_dashboard, name='operator_dashboard'),
    path('queue_operator/', views.queue_operator_view, name='queue_operator_view'),
    path('queue/<int:queue_id>/', views.queue_detail, name='queue_detail'),
    path('serve_guest/<int:guest_id>/', views.serve_guest, name='serve_guest'),
    path('remove_guest/<int:guest_id>/', views.remove_guest, name='remove_guest'),
    path('', views.homepage, name='homepage'),
    path("forbidden/", views.forbidden_view, name="forbidden"),
    path('contact/', views.contact, name='contact'),

]