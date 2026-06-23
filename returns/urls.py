from django.urls import path
from .views import ReturnRefundListCreateAPIView ,UpdateReturnStatusAPIView, ReturnHistoryAPIView

urlpatterns = [
    path(
        "",
        ReturnRefundListCreateAPIView.as_view()
    ),
     path(
        "<int:return_id>/status/",
        UpdateReturnStatusAPIView.as_view()
    ),
    path(
    "history/",
    ReturnHistoryAPIView.as_view()
    ),

]