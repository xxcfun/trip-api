from system.serializers import BaseImageSerializer
from utils.serializers import BaseListPageSerializer, BaseSerializer


class SightListSerializer(BaseListPageSerializer):
    """ 景点列表 """

    def get_object(self, obj):
        return {
            'id': obj.id,
            'name': obj.name,
            'main_img': obj.main_img.url,
            'score': obj.score,
            'province': obj.province,
            'city': obj.city,
            'min_price': obj.min_price,
            'comment_count': obj.comment_count
        }


class SightDetailSerializer(BaseSerializer):
    """ 景点详情 """

    def to_dict(self):
        obj = self.obj
        return {
            'id': obj.id,
            'name': obj.name,
            'desc': obj.desc,
            'img': obj.banner_img.url,
            'content': obj.content,
            'score': obj.score,
            'min_price': obj.min_price,
            'province': obj.province,
            'city': obj.city,
            'area': obj.area,
            'town': obj.town,
            'comment_count': obj.comment_count,
            'image_count': obj.image_count
        }


class CommentListSerializer(BaseListPageSerializer):
    """ 评论列表 """

    def get_object(self, obj):
        user = obj.user
        images = []
        for image in obj.images.filter(is_valid=True):
            images.append(BaseImageSerializer(image).to_dict())
        return {
            'pk': obj.pk,
            'user': {
                'pk': user.pk,
                'nickname': user.nickname
            },
            'content': obj.content,
            'is_top': obj.is_top,
            'love_count': obj.love_count,
            'score': obj.score,
            'is_public': obj.is_public,
            'images': images,
            'created_at': obj.created_at.strftime('%Y-%m-%d')
        }


class TicketListSerializer(BaseListPageSerializer):
    """ 门票列表 """

    def get_object(self, obj):
        return {
            'pk': obj.pk,
            'name': obj.name,
            'desc': obj.desc,
            'types': obj.types,
            'price': obj.price,
            'sell_price': obj.sell_price,
            'discount': obj.discount,
            'total_stock': obj.total_stock,
            'remain_stock': obj.remain_stock
        }


class SightInfoSerializer(BaseSerializer):
    """ 景点介绍 """

    def to_dict(self):
        obj = self.obj
        return {
            'pk': obj.sight.pk,
            'entry_explain': obj.entry_explain,
            'play_way': obj.play_way,
            'tips': obj.tips,
            'traffic': obj.traffic,
        }


class ImageListSerializer(BaseSerializer):
    """ 景点下的图片列表 """

    def get_object(self, obj):
        images = []
        for image in obj.images.filter(is_valid=True):
            images.append(BaseImageSerializer(image).to_dict())

        return images


# TODO 景点下的所有图片
# class ImageListSerializer(BaseListPageSerializer):
#
#     def get_object(self, obj):
#         images = set()
#         for image in obj.images.filter(is_valid=True):
#             images.add(BaseImageSerializer(image))
#         images = dict(images)
#         print(images)
#         return images


class TicketDetailSerializer(BaseSerializer):
    """ 门票详情 """
    def to_dict(self):
        obj = self.obj
        return {
            'pk': obj.pk,
            'name': obj.name,
            'desc': obj.desc,
            'types': obj.types,
            'price': obj.price,
            'sell_price': obj.price,
            'discount': obj.discount,
            'expire_date': obj.expire_date,
            'return_policy': obj.return_policy,
            'has_invoice': obj.has_invoice,
            'entry_way': obj.get_entry_way_display(),
            'tips': obj.tips,
            'remark': obj.remark
        }