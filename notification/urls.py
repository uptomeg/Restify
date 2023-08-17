from django.urls import path
from .views import *

app_name = "notification"
urlpatterns = [
    path('all/', AllNotificationView.as_view(), name='allNotification'),
    # path('send/<int:userid>/', SendNotification.as_view(), name='sendNotification'),
    path('view/notification/<int:pk>/', SingleNotificationView.as_view(), name='singleNotification'),
    path('send/message/<int:pk>/', CreateMessageView.as_view(), name='createMessage'),
    # path('view/sent/<int:target_id>/', ViewSentMessage.as_view(), name='viewSent'),
    # path('view/get/<int:target_id>/', ViewReceivedMessage.as_view(), name='viewGet'),
    path('view/with/<int:target_id>/', ViewMessageWith.as_view(), name='viewMessageWith'),
    path('recent/', RecentMessageUserView.as_view(), name='recent_users'),
]
