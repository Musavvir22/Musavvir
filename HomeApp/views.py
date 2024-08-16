from rest_framework.decorators import api_view  
from rest_framework.response import Response
from .models import Person
from .serializers import PersonSerializer,LoginSerializer
from rest_framework.views import APIView
from rest_framework import viewsets
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





#  APIVIEW


class PersonAPI(APIView):

    def get(self,request):
        obj = Person.objects.filter(color__isnull=True)    

        serializer = PersonSerializer(obj,many=True)   
        return Response (serializer.data)
        # return Response({"message":"this is a get req APIVIEW based"})
    

    
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