from django.contrib.auth.models import Group, User
from rest_framework import serializers

# ######## test serializers ########
# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']  

# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']



# ######## app serializers ########
from .models import UserIndex, UserProfile
class UserIndexSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserIndex
        fields = '__all__'

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
    user = UserIndexSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user', 'total_investment', 'todays_profit_loss', 'profit_loss']

    # def create(self, validated_data):
    #     user_index = validated_data.pop('user')
    #     user_profile = UserProfile.objects.create(user=user_index, **validated_data)
    #     return user_profile
    