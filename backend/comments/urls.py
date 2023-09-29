from django.urls import path
from .views import *

app_name = "comments"
urlpatterns = [
    path('view/<int:pk>/', UserCommentView.as_view(), name='viewComment'),
    path('leave/<int:pk>/', LeaveComment.as_view(), name='leaveComment'),
    path('view/single/<int:pk>/', SingleComment.as_view(), name='viewSingleComment'),
    path('delete/<int:pk>/', DeleteUserComment.as_view(), name='deleteUserComment'),
    path('reply/<int:pk>/', ReplyUserComment.as_view(), name='replyUserComment'),
    path('update/<int:pk>/', UpdateUserComment.as_view(), name='updateUserComment'),

    path('createProperty/<int:pk>/', CreatePropertyComment.as_view(), name='createPropertyComment'),
    path('viewProperty/<int:pk>/', PropertyCommentView.as_view(), name='viewPropertyComment'),
    path('updateProperty/<int:pk>/', UpdatePropertyCommentView.as_view(), name='UpdatePropertyComment'),
    path('deleteProperty/<int:pk>/', DeletePropertyCommentView.as_view(), name='deletePropertyView'),
    path('replyProperty/<int:pk>/', ReplyPropertyComment.as_view(), name='replyPropertyComment'),
    path('viewProperty/single/<int:pk>/', SinglePropertyCommentView.as_view(), name='viewSinglePropertyComment'),
]
