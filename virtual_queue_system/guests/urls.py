from django.urls import path 
from . import views 


urlpatterns = [ 
    path('enter_queue/<int:queue_id>', views.guest_page, name='enter_queue'),
    path('guest_queue/<int:queue_id>/<int:guest_id>', views.queue_guest, name='queue_guest'),
    path('game/<int:queue_id>/<int:guest_id>/', views.game, name='game'),
    path('queue/refresh_status/<int:guest_id>/', views.refresh_queue_status, name='refresh_queue_status'),
    path("queue/walk_away/<int:guest_id>/", views.walk_away, name="walk_away"),  # New URL
    

]