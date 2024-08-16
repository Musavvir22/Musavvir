from rest_framework import serializers
from .models import Person,Color




class LoginSerializer(serializers.Serializer):
   email = serializers.EmailField()
   password = serializers.CharField(max_length=100)





class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['color_name']



class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        color = ColorSerializer()
        color_info = serializers.SerializerMethodField()




    class Meta:
        model = Person
        fields = '__all__'
        depth = 1

    def get_color_info(self,obj):
     color_obj = Color.objects.get(id = obj.color.id)

     return {'color_name': color_obj.color_name,'hex_code':'0000'}