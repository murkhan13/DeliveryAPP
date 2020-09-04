from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'name', 'phone',)
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    # user_exists = serializers.SerializerMethodField('user_existing')

    class Meta:
        model = User
        fields = ('id', 'phone', 'name')
    
    def user_existing(self, user):
        user_exsts = User.objects.filter(phone__iexact=user.phone)
        if user_exsts.exists():
            user_exsts = True
        else: 
            user_exsts = False
        return user_exsts


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()


    def validate(self, data):

        phone = data.get('phone')
        user_exists = User.objects.filter(phone__iexact=phone)
        if user_exists is not None:
            user_exists = True
        else:
            user_exists = False

        if phone :
            if User.objects.filter(phone = phone).exists():
                user = User.objects.get(phone = phone)
                print('details:', user.id)
                # user = authenticate( request = self.context.get('request'), phone=phone)
                print("user:",user)
            else:
                msg = {
                    'detail': 'Phone number not found',
                    'status': False
                }
                raise serializers.ValidationError(msg)
            if not user:
                msg = {
                    'detail': 'Phone number and name are not matching, Try again',
                    'status': 'False'
                }
                raise serializers.ValidationError(msg, code= 'authorization')
        else:
            msq = {
                'detail': "Phone number and name weren't found in request",
                'status': False
            }
            raise serializers.ValidationError(msg, code='authorization')
        
        data['user'] = user
        data['user_exists'] = (user_exists)
        return data


        
    