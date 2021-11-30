from rest_framework import response
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes, schema
from .serializers import CustomUserSerializer,ChangePasswordSerializer,LoginSerializer
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password, check_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import ValidationError
from drf_yasg import openapi
from .models import CustomUser
from django.contrib.auth.signals import user_logged_in
# Create your views here.


User= get_user_model()
# Create your views here.
@swagger_auto_schema(methods=['POST'], request_body=CustomUserSerializer())
@api_view(['GET', 'POST'])

def users(request):

   
    if request.method == 'POST':
        serializer=CustomUserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['password']=make_password(serializer.validated_data['password'])
            
            user = User.objects.create(**serializer.validated_data)
            user_serializer = CustomUserSerializer(user)
            data={
            "message":"successfully created",
            "data": user_serializer.data
             }
        

            return Response(data,status=status.HTTP_201_CREATED)

        else:
            error ={
                "status": False,
                "message":'failed',
                "errors":serializer.errors
            }

            return Response(error, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def get_user(request):
    if request.method=='GET':
        user = User.objects.filter(is_active=True)

        serializer= CustomUserSerializer(user, many=True)
        data={
            'status':True,
            'message': 'Successful',
            'data': serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

@swagger_auto_schema(methods=['PUT','DELETE'], request_body=CustomUserSerializer())
@api_view(['GET','PUT','DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request,user_id):
    try:
        user =User.objects.get(id=request.user.id, is_active=True) #get the data from the model
    except User.DoesNotExist:
        error={
        'status':'false',
        'errors': f"user with id {user_id} does not exist"
    }
        return Response(error, status=status.HTTP_404_NOT_FOUND)
   
    if request.method=='GET':
        serializer=CustomUserSerializer(user)
        data={
            "message":"success",
            "data": serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

    elif request.method=='PUT':
        serializer=CustomUserSerializer(user,data=request.data,partial=True)
    

        if serializer.is_valid():
            if 'password' in serializer.validated_data.keys():
                raise ValidationError("unable to change password")

            serializer.save()
            data={
            "message":"success",
            "data": serializer.data
             }

            return Response(data, status=status.HTTP_202_ACCEPTED)
        
        
        else:
            error ={
                "message":'failed',
                "errors":serializer.errors
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

    elif request.method=='DELETE':
        user.is_active=False
        user.save()

        data={
            'status': True,
            'message': 'Deleted Successfully'
            }

        return Response(data, status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(methods=['POST'], request_body=openapi.Schema(type=openapi.TYPE_OBJECT,
properties={
    'username': openapi.Schema(type=openapi.TYPE_STRING,description='string'),
    'password': openapi.Schema(type=openapi.TYPE_STRING, description='string')
    }
))
@api_view(["POST"])
def Login(request):
    
    if request.method=="POST":
        user=authenticate(request, username=request.data['username'], password=request.data['password'])
        if user is not None:
            if user.is_active==True:
                try:
                    user_detail = {}
                    user_detail['id']   = user.id
                    user_detail['first_name'] = user.first_name
                    user_detail['last_name'] = user.last_name
                    user_detail['email'] = user.email
                    user_detail['username'] = user.username

                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)

                    data = {
                    'status'  : True,
                    'message' : "Successful",
                    'data' : user_detail,
                    }
                    return Response(data, status=status.HTTP_200_OK)

                except Exception as e:
                    raise e
            else:
                data = {
                'status'  : False,
                'error': 'This account has not been activated'
                }
            return Response(data, status=status.HTTP_403_FORBIDDEN)

        else:
            data = {
                'status'  : False,
                'error': 'Please provide a valid username and a password'
                }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)


@swagger_auto_schema(methods=['POST'], request_body=ChangePasswordSerializer())
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])   
def reset_password(request):
    """Allows users to edit password when logged in."""
    user = request.user
    if request.method == 'POST':
        serializer = ChangePasswordSerializer(data = request.data)
        if serializer.is_valid():
            if check_password(serializer.validated_data['old_password'], user.password):
                if serializer.check_pass():
                    user.set_password(serializer.validated_data['new_password'])
                    user.save()

                    data = {
                        'status'  : True,
                        'message': "Successfully saved password"
                        }
                    return Response(data, status=status.HTTP_202_ACCEPTED) 
                else:

                    data = {
                        'status'  : False,
                        'error': "Please enter matching passwords"
                        }
                    return Response(data, status=status.HTTP_400_BAD_REQUEST)   

            else:

                data = {
                    'status'  : False,
                    'error': "Incorrect password"
                    }
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)   


        else:

            data = {
                'status'  : False,
                'error': serializer.errors
                }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)   



@swagger_auto_schema(methods=['DELETE'], request_body=CustomUserSerializer())
@api_view(['GET', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def user_detail(request, user_id):
    """"""

    try:
        user = User.objects.get(id =user_id, is_active=True)

    except User.DoesNotExist:
        data = {
                'status'  : False,
                'message' : "Does not exist"
            }

        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomUserSerializer(user)

        data = {
                'status'  : True,
                'message' : "Successful",
                'data' : serializer.data,
            }

        return Response(data, status=status.HTTP_200_OK)

    #delete the account
    elif request.method == 'DELETE':
        user.is_active = False
        user.save()

        data = {
                'status'  : True,
                'message' : "Deleted Successfully"
            }

        return Response(data, status = status.HTTP_204_NO_CONTENT)
