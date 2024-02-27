from rest_framework import serializers
from .models import Person,Color

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField()
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