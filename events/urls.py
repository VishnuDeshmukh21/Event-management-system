from django.urls import path
from .views import event_find,event_add,hello
urlpatterns = [
    path('find',event_find),
    path('add',event_add),
    path('',hello)
]
