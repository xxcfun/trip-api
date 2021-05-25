import random
import re

from django import forms
from django.core.cache import cache

from utils import constants


class SendSmsCodeForm(forms.Form):
    """ 发送验证码的表单 """
    phone_num = forms.CharField(label='手机号码', required=True, error_messages={
        'required': '请输入手机号码'
    })

    def clean_phone_num(self):
        """ 验证是否为手机号 """
        phone_num = self.cleaned_data['phone_num']
        pattern = r'^1[0-9]{10}$'
        if not re.search(pattern, phone_num):
            raise forms.ValidationError('手机号%s输入不正确', code='invalid_phone', params=(phone_num, ))
        return phone_num

    def send_sms_code(self):
        """ 生成验证码 """
        sms_code = random.randint(100000, 999999)
        phone_num = self.cleaned_data.get('phone_num', None)
        try:
            # TODO 在实际场景中，要调用发送验证码的短信接口
            # redis中的key
            key = '{}{}'.format(constants.REGISTER_SMS_CODE_KEY, phone_num)
            # 将验证码存入redis
            timeout = 5 * 60
            cache.set(key, sms_code, timeout=timeout)
            return {
                'phone_num': phone_num,
                'sms_code': sms_code,
                'timeout': timeout
            }
        except Exception as e:
            print(e)
            return None
