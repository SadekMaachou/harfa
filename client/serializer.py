from rest_framework import serializers
from .models import artiste,product,Comment,Annonce,panier,Message
from django.contrib.auth.models import User

class standard_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']

class Artiste_Serializer(serializers.ModelSerializer):
    # Define fields from the related User model
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = artiste
        fields = ['username', 'email', 'preuve', 'profession']



class login_serializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=User
        fields=["email",'password']

class product_home_serializer(serializers.ModelSerializer):
    photo1 = serializers.ImageField()
    class Meta:
        model=product
        fields=['photo1', 'prodect_owner', 'price', 'product_name']

class annonce_home_serializer(serializers.ModelSerializer):
    photo1 = serializers.ImageField()
    class Meta:
        model=Annonce
        fields=['titre', 'likes', 'photo1','id']

class user_info_serializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username']


class All_Message_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Message
        fields='__all__'

class All_message_serializer_receive(serializers.ModelSerializer):
    class Meta:
        model:Message
        fields=['content','sender','receiver']
    


