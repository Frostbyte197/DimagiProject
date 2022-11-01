from django.urls import path
from .views import *

urlpatterns = [
    path('location/', LocationRecordListCreateAPIView.as_view(), name='location_record-post-list'),
]