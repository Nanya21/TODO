from rest_framework import serializers
from . models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model=CustomUser
        fields= '__all__'

class LoginSerializer(serializers.Serializer):
    username= serializers.CharField(max_length=500)
    password= serializers.CharField(max_length=500)
    

class ChangePasswordSerializer(serializers.Serializer):
    old_password= serializers.CharField(max_length=500)
    new_password= serializers.CharField(max_length=500)
    re_password= serializers.CharField(max_length=500)

    def validate_password(self):
        if self.validated_data['new_password']!= self.validated_data['re_password']:
            raise serializers.ValidationError("Please enter matching passwords")
        return True

    # def validate_password(self, value):
    #     if value is self.initial_data['re_password']:
    #         raise serializers.ValidationError('Please enter matching passwords')
    #     return value