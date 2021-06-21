from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import BorrowedBookSerializer
from catalog.models import BookInstance

# Create your views here.
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def simpleapi(request):
    return Response({'text':'Hello world, This is your first api call'}, status=HTTP_200_OK)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
	username = request.data.get("username")
	password = request.data.get("password")
	if username is None or password is None:
		return response({'error' : 'Please provide both username and password'}, 
			status=HTTP_400_BAD_REQUEST)
	user = authenticate(username=username, password=password)
	if not user:
		return response({'error' : 'Invalid Credentials'}, 
			status=HTTP_404_NOT_FOUND)
	token, _ =Token.objects.get_or_create(user=user)
	return Response({'token' : token.key}, status = HTTP_200_OK)


@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def borrowedbooks(request):
    queryset = BookInstance.objects.filter(borrower=request.user).filter(status__exact='o').order_by('due_back')
    serializer = BorrowedBookSerializer(queryset,many=True)
    return Response(serializer.data,status=HTTP_200_OK)