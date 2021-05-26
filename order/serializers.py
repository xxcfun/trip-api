from utils.serializers import BaseSerializer, BaseListPageSerializer


class OrderItemSerializer(BaseSerializer):
    """ 订单明细 """
    def to_dict(self):
        obj = self.obj
        return {
            'pk': obj.pk,
            'flash_name': obj.flash_name,
            'flash_img': obj.flash_img.url,
            'flash_price': obj.flash_price,
            'flash_origin_price': obj.flash_origin_price,
            'flash_discount': obj.flash_discount,
            'count': obj.count,
            'amount': obj.amount,
            'status': obj.status,
            'remark': obj.remark,
            'object_id': obj.object_id,
            'app_label': obj.content_type.app_label,
            'model': obj.content_type.model
        }


class OrderDetailSerializer(BaseSerializer):
    """ 订单详细信息 """
    def to_dict(self):
        obj = self.obj
        items = []
        for item in obj.order_items.all():
            items.append(OrderItemSerializer(item).to_dict())
        return {
            'sn': obj.sn,
            'buy_amount': obj.buy_amount,
            'buy_count': obj.buy_count,
            'to_user': obj.to_user,
            'to_area': obj.to_area,
            'to_address': obj.to_address,
            'to_phone': obj.to_phone,
            'remark': obj.remark,
            'express_type': obj.express_type,
            'express_no': obj.express_no,
            'status': obj.status,
            'types': obj.types,
            'created_at': obj.created_at,
            'items': items
        }


class OrderListSerializer(BaseListPageSerializer):
    """ 订单列表 """
    def get_object(self, obj):
        item_first_obj = obj.order_items.first()
        item_first = OrderItemSerializer(item_first_obj).to_dict()
        return {
            'sn': obj.sn,
            'buy_amount': obj.buy_amount,
            'buy_count': obj.buy_count,
            'types': obj.types,
            'status': obj.status,
            'remark': obj.remark,
            'created_at': obj.created_at,
            'item_first': item_first
        }
