from utils.serializers import BaseSerializer


class UserSerializers(BaseSerializer):
    """ 用户基础信息 """
    def to_dict(self):
        user = self.obj
        return {
            'username': user.username,
            'nickname': user.nickname,
            'avatar': user.avatar_url
        }


class UserProfileSerializer(BaseSerializer):
    """ 用户的详细信息 """
    def to_dict(self):
        profile = self.obj
        return {
            'real_name': profile.real_name,
            'sex': profile.sex,
            'sex_display': profile.get_sex_display()
        }
