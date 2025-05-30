from django.urls import path
from .views import thing_list, delete_thing

app_name = 'things'

urlpatterns = [
    path('things', thing_list, name='thing_list'),
    path('delete/<int:thing_id>/', delete_thing, name='delete'),
]
