import json

from django import http
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from order.forms import SubmitTicketOrderForm
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
