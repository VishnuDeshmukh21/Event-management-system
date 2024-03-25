from django.urls import path
from .views import event_find,event_add
urlpatterns = [
    path('',event_find),
    path('add',event_add)
]
