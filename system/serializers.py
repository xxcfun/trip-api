from utils.serializers import BaseSerializer


class BaseImageSerializer(BaseSerializer):
    """ 序列化基础图片：其它列表需要引用到时使用 """

    def to_dict(self):
        return {
            'img': self.obj.img.url,
            'summary': self.obj.summary
        }
