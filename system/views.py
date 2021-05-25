import json

from django import http
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import FormView

from system.forms import SendSmsCodeForm
from system.models import Slider
from utils.response import ServerErrorJsonResponse, BadRequestJsonResponse


def slider_list(request):
    data = {
        'meta': {

        },
        'objects': []
    }
    queryset = Slider.objects.filter(is_valid=True)
    for item in queryset:
        data['objects'].append({
            'id': item.id,
            'img_url': item.img.url,
            'target_url': item.target_url,
            'name': item.name
        })
    # return HttpResponse('ok')
    return http.JsonResponse(data)


def cache_set(request):
    return HttpResponse('ok')


def send_sms(request):
    pass
    # 拿到手机号，判断是否为真实的手机号码
    # 生成验证码并存储
    # TODO 调用短信的发送接口
    # 告诉用户验证码是否发送成功


class SmsCodeView(FormView):
    form_class = SendSmsCodeForm

    def form_valid(self, form):
        """ 表单通过验证 """
        data = form.send_sms_code()
        if data is not None:
            return http.JsonResponse(data, status=201)
        return ServerErrorJsonResponse()

    def form_invalid(self, form):
        """ 表单没有通过验证 """
        err_list = json.loads(form.errors.as_json())
        return BadRequestJsonResponse(err_list)
