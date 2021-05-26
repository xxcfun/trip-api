import json

from django import http
from django.db import transaction
from django.db.models import F
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import FormView
from django.views.generic.detail import BaseDetailView

from order import serializers
from order.choices import OrderStatus
from order.forms import SubmitTicketOrderForm
from order.models import Order
from utils.response import BadRequestJsonResponse
from utils.views import login_required


def ticket_submit(request):
    """ 门票下单接口 """
    # 验证用户是否已经登录
    # 获取post数据
    # 数据验证
    # 关联用户、生成订单号、计算购买总价、生成订单（order）
    # 返回内容：订单id
    pass


@method_decorator(login_required, name='dispatch')
class TicketOrderSubmitView(FormView):
    """ 门票订单接口 """
    form_class = SubmitTicketOrderForm
    http_method_names = ['post']

    def form_invalid(self, form):
        """ 表单未通过验证 """
        err = json.loads(form.errors.as_json())
        return BadRequestJsonResponse(err)

    def form_valid(self, form):
        """ 表单通过验证 """
        obj = form.save(user=self.request.user)
        return http.JsonResponse({
            'sn': obj.sn
        }, status=201)


@method_decorator(login_required, name='dispatch')
class OrderDetail(BaseDetailView):
    slug_field = 'sn'
    slug_url_kwarg = 'sn'

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user, is_valid=True)

    def get(self, request, *args, **kwargs):
        """ GET：订单详情 """
        order_obj = self.get_object()
        data = serializers.OrderDetailSerializer(order_obj).to_dict()
        return http.JsonResponse(data)

    def post(self, request, *args, **kwargs):
        """ POST：订单支付 """
        # 选择支付方式
        # 数据验证
        order_obj = self.get_object()
        if order_obj.status == OrderStatus.SUBMIT:
            # 调用真实的支付
            # 改变订单状态
            order_obj.status = OrderStatus.PAID
            order_obj.save()
            order_obj.order_items.update(status=OrderStatus.PAID)
            return http.HttpResponse('', status=201)
        return http.HttpResponse('', status=200)

    def delete(self, request, *args, **kwargs):
        """ DELETE：订单删除 """
        # 获取订单对象
        order_obj = self.get_object()
        # 数据验证（已经支付，已经取消）
        if order_obj.status == OrderStatus.CANCELED or order_obj.status == OrderStatus.PAID:
            # 是否已经删除过了
            if order_obj.is_valid:
                order_obj.is_valid = False
                order_obj.save()
                return http.HttpResponse('', status=201)
            else:
                # 由于上面已过滤False字段，所以此处不做配置，由get_queryset触发404
                pass
        return http.HttpResponse('', status=200)

    @transaction.atomic()
    def put(self, request, *args, **kwargs):
        """ PUT：订单取消 """
        # 获取订单对象
        order_obj = self.get_object()
        # 数据验证，状态判断
        if order_obj.status == OrderStatus.SUBMIT:
            # 改变状态
            order_obj.status = OrderStatus.CANCELED
            order_obj.save()
            items = order_obj.order_items.filter(status=OrderStatus.SUBMIT)
            # 加回已经扣减的库存
            for item in items:
                obj = item.content_object
                obj.remain_stock = F('remain_stock') + item.count
                obj.save()
            items.update(status=OrderStatus.CANCELED)
            return http.HttpResponse('', status=201)
        return http.HttpResponse('', 200)
