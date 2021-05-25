from django.urls import path

from accounts import views

urlpatterns = [
    # 用户登入
    path('user/api/login/', views.user_api_login, name='user_api_login'),
    # 用户登出
    path('user/api/logout/', views.user_api_logout, name='user_api_logout'),
    # 用户详细信息接口
    path('user/api/info/', views.UserDetailView.as_view(), name='user_api_info'),
    # 用户的注册
    path('user/api/register/', views.UserRegisterView.as_view(), name='user_api_register'),
]
