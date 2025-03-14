from django.urls import path 
from . import views 


urlpatterns = [ 
    path('signup/manager/',  views.manager_signup,  name='manager_signup'),
    path('signup/operator/', views.operator_signup, name='operator_signup'),
    path('login',            views.user_login,      name='login'),
    path('logout/',          views.user_logout,     name='logout'),


    path('dashboard',          views.manager_dashboard,  name='manager_dashboard'),
    path('operator_dashboard', views.operator_dashboard, name='operator_dashboard'),
    path('create_queue',       views.create_queue,       name='create_queue'),

]