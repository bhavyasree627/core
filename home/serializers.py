from rest_framework import serializers
from .models import Person,Color
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password=serializers.CharField()

    def validate(self, data):

        if data['username']:
            if User.objects.filter(username = data['username']).exists():
                raise serializers.ValidationError('Username is taken')
        
        if data['email']:
            if User.objects.filter(email= data['email']).exists():
                raise serializers.ValidationError('Email is taken')
        return data

    def create(self,validated_data):
        user=User.objects.create_user(username=validated_data['username'],email=validated_data["email"])
        user.set_password(validated_data['password'])
        user.save()
        print(validated_data)
        return validated_data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password=serializers.CharField()

# class ColorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Color
#         fields=["color_name"]
class PeopleSerializer(serializers.ModelSerializer):
    # color=ColorSerializer()
    # color_info=serializers.SerializerMethodField()
    class Meta:
        model = Person
        fields = '__all__'  #gets all the fields
        # depth=1
    # def get_color_info(self,obj):
    #     color_obj=Color.objects.get(id=obj.color.id)
    #     return {"color_name":color_obj.color_name,"hex_code":"#000"}

    def validate_name(self,data):
        if not data.isalpha():
            raise serializers.ValidationError("Name can only contain letters.")
        return data
    def validate_age(self,data):
        if data<18:
            raise serializers.ValidationError("Age should be greater than 18")
        return data