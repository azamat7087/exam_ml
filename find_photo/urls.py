from django.urls import path, include
from .views import *


urlpatterns = [
    path("", Main.as_view(), name='main'),
    path("group/<int:id>", GroupDetail.as_view(), name='group_detail'),

]
