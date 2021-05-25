import json

from django import http
from django.contrib.auth import logout
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView

from accounts import serializers
from accounts.forms import LoginForm, RegisterForm
from utils.response import BadRequestJsonResponse, MethodNotAllowedJsonResponse, UnauthorizedJsonResponse, \
    ServerErrorJsonResponse


def user_api_login(request):
    """ 用户登录接口-POST """
    if request.method == 'POST':
        # 表单验证
        form = LoginForm(request.POST)
        # 如果通过了验证，执行登录
        if form.is_valid():
            user = form.do_login(request)
            profile = user.profile
            # 返回内容：用户的信息（用户的基本信息、详细信息）
            data = {
                'user': serializers.UserSerializers(user).to_dict(),
                'profile': serializers.UserProfileSerializer(profile).to_dict()
            }
            return http.JsonResponse(data)
        else:
            # 如果没有通过表单验证，返回表单的错误信息
            err = json.loads(form.errors.as_json())
            return BadRequestJsonResponse(err)
    else:
        # 请求不被允许
        return MethodNotAllowedJsonResponse()


def user_api_logout(request):
    """ 用户推出接口 """
    logout(request)
    return http.HttpResponse(status=201)


class UserDetailView(View):
    """ 用户详细接口 """

    def get(self, request):
        # 获取用户信息
        user = request.user
        # 用户：是游客吗？
        if not user.is_authenticated:
            # 返回401状态码
            return UnauthorizedJsonResponse()
        else:
            # 返回详细信息
            profile = user.profile
            data = {
                'user': serializers.UserSerializers(user).to_dict(),
                'profile': serializers.UserProfileSerializer(profile).to_dict()
            }
            return http.JsonResponse(data)


def user_api_register(request):
    """ 用户注册 """
    pass
    # 表单，验证用户输入的信息
    # 创建用户基础信息表，用户详细信息表
    # 执行登录
    # 保存登录日志
    # TODO 流程，具体方法见下面


class UserRegisterView(FormView):
    """ 用户注册 """
    form_class = RegisterForm
    http_method_names = ['post']

    def form_valid(self, form):
        """ 表单已经通过验证 """
        result = form.do_register(request=self.request)
        if result is not None:
            user, profile = result
            data = {
                'user': serializers.UserSerializers(user).to_dict(),
                'profile': serializers.UserProfileSerializer(profile).to_dict()
            }
            return http.JsonResponse(data, status=201)
        return ServerErrorJsonResponse()

    def form_invalid(self, form):
        """ 表单没有通过验证 """
        err_list = json.loads(form.errors.as_json())
        return BadRequestJsonResponse(err_list)
