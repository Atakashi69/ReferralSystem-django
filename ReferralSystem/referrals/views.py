import random
import string
import time
import uuid

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from .models import Profile
from .serializers import ProfileSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if Profile.objects.filter(username=username).exists():
            return Response({'error': 'This phone number is already in use.'}, status=status.HTTP_400_BAD_REQUEST)

        time.sleep(2)

        auth_code = ''.join(random.choices(string.digits, k=4))

        user = Profile.objects.create_user(username=username, password=password, auth_code=auth_code)
        user = authenticate(username=username, password=password)

        return Response({'message': 'Code sent successfully', 'code': auth_code}, status=status.HTTP_200_OK)


class VerificationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        username = data.get('username')
        auth_code = data.get('auth_code')

        if not username or not auth_code:
            return Response({'error': 'Username and code are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = Profile.objects.filter(username=username).first()

        if not user:
            return Response({'error': 'Invalid phone number.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.auth_code is None:
            return Response({'error': 'Profile already verified.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.auth_code != auth_code:
            return Response({'error': 'Invalid auth code.'}, status=status.HTTP_400_BAD_REQUEST)

        user.auth_code = None
        user.invite_code = str(uuid.uuid4()).replace("-", "")[:6]
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'message': 'Profile verified', 'token': token.key, 'invite_code': user.invite_code}, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)

        return Response({'token': token.key}, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)


class ActivationView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = request.data
        user = request.user
        invite_code = data.get('invite_code')

        if user.referral:
            return Response({'error': 'Invite code already activated.'}, status=status.HTTP_400_BAD_REQUEST)

        referral = Profile.objects.filter(invite_code=invite_code).first()
        if not referral and invite_code != user.invite_code:
            return Response({'error': 'Invalid invite code'}, status=status.HTTP_400_BAD_REQUEST)

        user.referral = referral
        user.save()

        return Response({'message': 'Code activated successfully'}, status=status.HTTP_200_OK)

