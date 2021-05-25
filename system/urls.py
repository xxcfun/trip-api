from django.urls import path

from system import views

urlpatterns = [
    # 轮播图接口
    path('slider/list/', views.slider_list, name='slider_list'),
    # caches
    path('cache/set/', views.cache_set, name='cache_set'),
    # 发送验证码
    path('send/sms/', views.SmsCodeView.as_view(), name='send_sms'),
]