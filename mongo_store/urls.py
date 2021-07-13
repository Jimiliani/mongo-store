from django.contrib import admin
from django.urls import path

from main.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('items/', get_multiple_items_or_create),
    path('items/<str:pk>/', get_item),
    path('items/<str:pk>/buy/', buy_item),
]
