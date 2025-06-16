from django.shortcuts import render


from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
# from django.contrib.auth.models import Group, User
from rest_framework import viewsets, permissions
# from .serializers import UserSerializer, GroupSerializer

from .serializers import UserIndexSerializer, UserProfileSerializer
from .models import UserIndex, UserProfile


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]

# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]




class UserIndexViewSet(APIView):
    """
    API endpoint that allows user indices to be viewed or edited.
    """
    queryset = UserIndex.objects.all().order_by('id')
    serializer_class = UserIndexSerializer
    def get(self,request, *args, **kwargs):
        # user_indices = UserIndex.objects.all().order_by('id')
        # serializer = UserIndexSerializer(user_indices, many=True)
        # return Response(serializer.data)
        return Response({"message": "Welcome to User Index API"})
    

    # permission_classes = [permissions.IsAuthenticated]

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows user profiles to be viewed or edited.
    """
    queryset = UserProfile.objects.all().order_by('user__username')
    serializer_class = UserProfileSerializer

    # permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Automatically set the user to the logged-in user


