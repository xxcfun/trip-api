from django.urls import path

from order import views

urlpatterns = [
    # 订单提交接口
    path('ticket/submit/', views.TicketOrderSubmitView.as_view(), name='ticket_submit'),
    # 订单详情
    path('order/detail/<int:sn>/', views.OrderDetail.as_view(), name='order_detail')
]