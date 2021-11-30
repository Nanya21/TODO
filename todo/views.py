from rest_framework.exceptions import PermissionDenied
from .models import Todo
from .serializers import Todoserializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
@swagger_auto_schema(methods=['POST'], request_body=Todoserializer())
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET' ,'POST'])
def todos(request):

    if request.method == 'GET':
        all_todos= Todo.objects.filter(user=request.user) #get the data

        serializer=Todoserializer(all_todos, many=True)
        #serialize the data

        data={
            "message":"success",
            "data": serializer.data
        }
        #prepare the response data
        return Response(data,status=status.HTTP_200_OK)
   
    elif request.method == 'POST':
        serializer=Todoserializer(data=request.data)

        if serializer.is_valid():
            if 'user' in serializer.validated_data.keys():
                serializer.validated_data.pop('user')

            object=Todo.objects.create(**serializer.validated_data, user=request.user)
            serializer=Todoserializer(object)

            data={
            "message":"successfully created",
            "data": serializer.data
             }
        

            return Response(data,status=status.HTTP_201_CREATED)

        else:
            error ={
                "message":'failed',
                "errors":serializer.errors
            }

            return Response(error, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(methods=['PUT', 'DELETE'], request_body=Todoserializer())
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail(request, todo_id):
   
    try:
        obj = Todo.objects.get(id = todo_id)
    
    except Todo.DoesNotExist:
        data = {
                'status'  : False,
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)
    if obj.user!=request.user:
        raise PermissionDenied(detail='You do not have permission to perform this action')


    if request.method == 'GET':
        serializer = Todoserializer(obj)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    #Update the profile of the TODO
    elif request.method == 'PUT':
        serializer = Todoserializer(obj, data = request.data, partial=True) 

        if serializer.is_valid():
        
            serializer.save()

            data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def mark_complete(request, todo_id):
   
    try:
        obj = Todo.objects.get(id = todo_id)
    
    except Todo.DoesNotExist:
        data = {
                'status'  : False,
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)
    if obj.user!=request.user:
        raise PermissionDenied(detail='You do not have permission to perform this action')


    if request.method == 'GET':
        serializer = Todoserializer(obj)
        
        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    #Update the profile of the TODO
    elif request.method == 'PUT':
        serializer = Todoserializer(obj, data = request.data, partial=True) 

        if serializer.is_valid():
        
            serializer.save()

            data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

            return Response(data, status = status.HTTP_201_CREATED)

        else:
            data = {
                'status'  : False,
                'message' : "Unsuccessful",
                'error' : serializer.errors,
            }

            return Response(data, status = status.HTTP_400_BAD_REQUEST)
