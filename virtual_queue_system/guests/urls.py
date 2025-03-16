from django.urls import path 
from . import views 


urlpatterns = [ 
    path('enter_queue/<int:queue_id>', views.guest_page, name='enter_queue'),
    path('guest_queue/<int:queue_id>/<int:guest_id>', views.queue_guest, name='queue_guest'),

]