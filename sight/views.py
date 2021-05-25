from django import http
from django.db.models import Q
from django.views.generic import ListView, DetailView

from sight import serializers
from sight.models import Sight, Comment, Ticket, Info
from utils.response import NotFoundJsonResponse


class SightListView(ListView):
    """ 景点列表 """
    # 每页放5条数据
    paginate_by = 10

    def get_queryset(self):
        """ 重写查询方法 """
        query = Q(is_valid=True)
        # 1.热门景点
        is_hot = self.request.GET.get('is_hot', None)
        if is_hot:
            query = query & Q(is_hot=True)
        # 2.精选景点
        is_top = self.request.GET.get('is_top', None)
        if is_top:
            query = query & Q(is_top=True)
        # 3.景点名称搜索
        name = self.request.GET.get('name', None)
        if name:
            query = query & Q(name__icontains=name)
        queryset = Sight.objects.filter(query)
        return queryset

    def get_paginate_by(self, queryset):
        """ 从前端控制每一页的分页大小 """
        page_size = self.request.GET.get('limit', None)
        return page_size or self.paginate_by

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['page_obj']
        if page_obj is not None:
            data = serializers.SightListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        else:
            return NotFoundJsonResponse()


class SightDetailView(DetailView):
    """ 景点详情信息 """
    def get_queryset(self):
        return Sight.objects.all()

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['object']
        if page_obj is not None:
            if page_obj.is_valid == False:
                return NotFoundJsonResponse()
            data = serializers.SightDetailSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


class SightCommentListView(ListView):
    """ 景点下的评论列表 """
    paginate_by = 10

    def get_queryset(self):
        """ 根据景点id查询景点 """
        sight_id = self.kwargs.get('pk', None)
        sight = Sight.objects.filter(pk=sight_id, is_valid=True).first()
        if sight:
            # return Comment.objects.filter(is_valid=True, sight=sight) # 下面这一行是代表了反向查询
            return sight.comments.filter(is_valid=True)
        return Comment.objects.none()

    def render_to_response(self, context, **response_kwargs):
        """ 重写响应的返回 """
        page_obj = context['page_obj']
        if page_obj is not None:
            data = serializers.CommentListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


class SightTicketListView(ListView):
    """ 景点下的门票列表 """
    paginate_by = 10

    def get_queryset(self):
        """ 根据景点id查询景点 """
        sight_id = self.kwargs.get('pk', None)
        return Ticket.objects.filter(is_valid=True, sight__id=sight_id)

    def render_to_response(self, context, **response_kwargs):
        """ 重写响应的返回 """
        page_obj = context['page_obj']
        if page_obj is not None:
            data = serializers.TicketListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


class SightInfoDetailView(DetailView):
    """ 景点介绍 """
    # slug_field = 'sight__pk'

    def get_queryset(self):
        return Info.objects.all()

    def render_to_response(self, context, **response_kwargs):
        page_obj = context['object']
        if page_obj is not None:
            data = serializers.SightInfoSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()


class SightImageListView(ListView):
    """ 景点下的图片列表 """
    paginate_by = 10

    def get_queryset(self):
        sight_id = self.kwargs.get('pk', None)
        sight = Sight.objects.filter(pk=sight_id, is_valid=True)
        return sight

    def render_to_response(self, context, **response_kwargs):
        """ 重写响应的返回 """
        page_obj = context['page_obj']
        if page_obj is not None:
            data = serializers.ImageListSerializer(page_obj).to_dict()
            return http.JsonResponse(data)
        return NotFoundJsonResponse()
