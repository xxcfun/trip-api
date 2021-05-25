from django.db import models


class TicketTypes(models.IntegerChoices):
    """ 门票类型 """
    ADULT = 11, '成人票'
    CHILD = 12, '儿童票'


class TicketStatus(models.IntegerChoices):
    """ 门票状态 """
    OPEN = 1, '开放购买'
    CLOSED = 0, '暂未开放'


class EntryWay(models.IntegerChoices):
    """ 入园方式 """
    BY_TICKET = 0, '短信换票入园'
    BY_CODE = 1, '凭借验证码入园'
