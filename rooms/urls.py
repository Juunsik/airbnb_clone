from django.urls import path
from . import views

app_name = "rooms"

# FBV=view.room_detail
urlpatterns = [path("<int:pk>", views.RoomDetail.as_view(), name="detail")]
