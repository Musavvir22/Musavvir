from rest_framework.decorators import api_view  
from rest_framework.response import Response
from .models import Person
from .serializers import PersonSerializer,LoginSerializer,RegisterSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status    
from django.contrib.auth import aauthenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.decorators import action
# Create your views here.


# api_view is a decorator means django function convert into json fun @deocrator modify the fun

@api_view(['GET','POST','PUT'])
def index(request):
    courses = {                         # json format key value pairs
        'course_name':'python',
        'learn' : ['DRF','fastAPI','flask'],
        'course_provider' :'scaler'
    }
    return Response(courses)  


from django.core.paginator import Paginator


#  APIVIEW


class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self,request):
        print(request.user)
        obj = Person.objects.filter(color__isnull=True) 

        page = request.GET.get('page',1)
        page_size = 3
        paginator = Paginator(obj,page_size)
        print(paginator.page(page))
        serializer = PersonSerializer(paginator.page(page),many=True)
        serializer = PersonSerializer(obj,many = True)
        return Response(serializer.data)
    
        # serializer = PersonSerializer(obj,many=True)   
        # return Response (serializer.data)
        # # return Response({"message":"this is a get req APIVIEW based"})
    

    
    def post(self,request):
        return Response({"message":"this is a post request APIVIEW"})
    
    def put(self,request):
        return Response({"message":"this is a put req APIVIEW "})
    

    
    def patch(self,request):
        return Response({"message":"this is a patch req APIVIEW"})
    
    
    def delete(self,request):
        return Response({"message":"this is a del req APIVIEW based"})






#  login

@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)

    if serializer.is_valid():
        data = serializer.data

        return Response({"message":"login Success"})



@api_view(["GET","POST","PUT","PATCH","DELETE"])
def person(request):
    if request.method =="GET":

        obj = Person.objects.filter(color__isnull=False)      # model class person .all   allfields store in obj

        serializer = PersonSerializer(obj,many=True)   # many=True for all objects 
        return Response (serializer.data)     # All data store in serializer.data & return Response
    

    elif request.method =="POST":
        data = request.data
        serializer = PersonSerializer(data=data)  # Serailizer check data if validate or not

        if serializer.is_valid():  # seriaizer is valid return true then save
            serializer.save() 
            return Response(serializer.data)
        return Response(serializer.errors)
    


    elif request.method =="PUT":       # All fields update PUT method
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj,data=data)

        if serializer.is_valid():
            serializer.save() 

            return Response(serializer.data)
        return Response(serializer.errors)
    


    elif request.method =="PATCH":   # Only Selected Fields required  PATCH method
        data = request.data
        obj = Person.objects.get(id=data['id'])
        serializer = PersonSerializer(obj,data=data,partial=True)

        if serializer.is_valid():
            serializer.save() 

            return Response(serializer.data)
        return Response(serializer.errors)


    else:
        data = request.data
        obj = Person.objects.get(id=data['id'])
        obj.delete()
        return Response({"message":"Person Delete"})




#  ViewSets

class PersonViewSet(viewsets.ModelViewSet):
    serializer_class = PersonSerializer
    queryset = Person.objects.all()
    http_method_names =['get','post']

    @action(detail=False, methods=['GET','post'])
    def send_mail_to_person(self,request,pk):
        obj = Person.objects.get(pk=pk)
        serializer = PersonSerializer(obj)
        return Response({
            'status': True,
            'message': 'Email sent successfully',
            'data' : serializer.data
            })


    # def list(self,request):    Later
    #     serializer_class =request.Get.get('search')
    #     queryset = self.queryset
    #     if search:
    #         queryset = queryset.filter(name_startswith = search)
        
    #     serializer = PersonSerializer(queryset,many=True)
    #     return Response({"message":200,'data' : serializer.data})


#  LoginAPI

class LoginAPI(APIView):

    def post(self,request):
        data = request.data

        serializer = LoginSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': 'serializer.errors'
            },status.HTTP_400_BAD_REQUEST)
        
        user =aauthenticate(username = serializer.data['username'],password = serializer.data['password'])

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"status":True,'message' :'user login','token':str(token)},status.HTTP_201_CREATED)






#  Register API


class RegisterAPI(APIView):
    
    def post(self,request):
        data = request.data
        serializer = RegisterSerializer(data=data)

        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': 'serializer.errors'
            },status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({"status":True,'message' :'user created'})

  


#    JWT JSON WEB TOKEN 
#  JWT  3 PARTS , JWT expire in few minuter and no one use then new jwt genrate