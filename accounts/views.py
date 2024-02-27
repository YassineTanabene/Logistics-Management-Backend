# accounts/views.py

from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from .serializers import UserSerializer,CamionSerializer
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Camion,CustomUser
from django.shortcuts import render
from rest_framework.parsers import FileUploadParser

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']

            # Check for duplicate email
            if CustomUser.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        # Ensure both email and password are provided
        if not email or not password:
            return Response({'error': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = None
        try:
            user = CustomUser.objects.get(email=email)
        except ObjectDoesNotExist:
            pass

        if user is not None and user.check_password(password):
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        




@api_view(['POST'])
def camion_create(request):
    # Create new Camion
    if request.method == 'POST':
        data = request.data

        # Ensure that quantity is less than or equal to capacity
        quantity = data.get('quantity')
        capacity = data.get('capacity')

        if quantity is not None and capacity is not None and quantity > capacity:
            return Response({'error': 'Quantity cannot be greater than capacity.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CamionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def camion_list(request):
    # List all camions
    if request.method == 'GET':
        camions = Camion.objects.all()
        serializer = CamionSerializer(camions, many=True, context={'request': request})  # Include request context for correct image URLs
        return Response(serializer.data, status=status.HTTP_200_OK)
    


@api_view(['DELETE'])
def camion_delete(request, id):
    try:
        camion = Camion.objects.get(id=id)
    except Camion.DoesNotExist:
        return Response({'message': 'Le Camion ne existe pas !'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'DELETE':
        camion.delete()
        return Response({'message': 'Le Camion est supprimé avec Succés !'},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def camion_retrieve(request,id):
    try:
        camion = Camion.objects.get(id=id)
    except Camion.DoesNotExist:
        return Response({'message': 'Le Camion ne existe pas !'}, status=status.HTTP_404_NOT_FOUND)

    if request.method=='GET':
        serializer = CamionSerializer(camion)
        return Response(serializer.data)


@api_view(['PUT'])
def camion_update(request,id):
    try:
        camion = Camion.objects.get(id=id)
    except Camion.DoesNotExist:
        return Response({'message': 'Le Camion ne existe pas !'}, status=status.HTTP_404_NOT_FOUND)

    if request.method=='PUT':
        serializer = CamionSerializer(camion, data=request.data)
        if serializer.is_valid():
            image_file = request.FILES.get('img')
            if image_file:
                camion.img = image_file
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET'])
def camion_list_published(request):
    # List all published camions
    camions = Camion.objects.filter(published=True)
    serializer = CamionSerializer(camions, many=True)
    return Response(serializer.data)       