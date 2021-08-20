import re

from rest_framework import serializers

from user.models import Worker


class worker_information_okXu(serializers.ModelSerializer):
    worker_type=serializers.SlugRelatedField(label='类别',slug_field='type_id',read_only='True')
    class Meta:
        model=Worker
        fields="__all__"
    def validate_worker_age(self,a):
        if int(a) <18 or int(a)>50:
            raise serializers.ValidationError('年龄不符合招聘标准!')
        return a
    def validate_worker_telephone(self, a):
        if not re.match('1[3-9]\d{9}',a):
            raise serializers.ValidationError('手机号码有误！')
        return a
    def validate_worker_idcard(self, attrs):
        if len(attrs)!=18:
            raise serializers.ValidationError('身份证号码错误！')
        return attrs

class pwd_updateXu(serializers.Serializer):
    oldPassword = serializers.CharField(max_length=8, label='密码',)
    newPassword = serializers.CharField(max_length=8, )
    reNewPassword = serializers.CharField(max_length=8, write_only=True)


    def validate_newPassword (self,a):
        if len(a)<6 or len(a)>18:
            raise serializers.ValidationError('密码格式错误')
        return a

    def update(self, instance, validated_data):
        instance.user_password=validated_data['newPassword']
        instance.save()
        return instance

