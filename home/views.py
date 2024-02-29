from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PeopleSerializer,LoginSerializer,RegisterSerializer
from .models import Person
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from django.core.paginator import Paginator
from rest_framework.decorators import action



class LoginAPI(APIView):

    def post(self,request):
        data=request.data
        serializer=LoginSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "status":False,
                "message":serializer.errors,
            },status.HTTP_400_BAD_REQUEST)

        print(serializer.data)
        user=authenticate(username=serializer.data['username'],password=serializer.data["password"])
        if not user:
            return Response({
                "status":False,
                "message":"user doesn't exist.",
            },status.HTTP_400_BAD_REQUEST)

        token, _ =Token.objects.get_or_create(user=user)
        print(token)
        return Response({"status":True,"message":"user_loggedIN","token":str(token)},status.HTTP_201_CREATED)


class RegisterAPI(APIView):
    def post(self,request):
        data=request.data
        serializer=RegisterSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "status":False,
                "message":serializer.errors,
            },status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"status":True,"message":"user_created"},status.HTTP_201_CREATED)


         

@api_view(['GET','POST','PUT'])
def index(request):
    courses={
            "course_name" : "Python",
            "learn" : ["Flask", "Django", "Tornado", "FastApi"],
            "course_provider" : "Scaler"
        }

    if request.method == "GET":
        print(request.GET.get('search'))
        print("You hit a GET method")
        return Response(courses)

    elif request.method == "POST":
        data=request.data
        print("********")
        print(data)
        print("********")
        print("You hit a POST method")
        return Response(courses)
    
    elif request.method == "PUT":
        print("You hit a PUT method")
        return Response(courses)

@api_view(["POST"])
def login(request):
    data=request.data
    serializer=LoginSerializer(data=data)

    if serializer.is_valid():
        data=serializer.validated_data
        print(data)
        return Response({"message":"success"})
    return Response(serializer.errors)


class PersonAPI(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[TokenAuthentication]
    def get(self,request):
        try:
            print(request.user)
            objs=Person.objects.all()
            page=request.GET.get('page',1)
            page_size=2
            paginator=Paginator(objs,page_size)
            serializer = PeopleSerializer(paginator.page(page), many = True)
            return Response(serializer.data)
        except Exception as e:
            return Response({
                "status" : False,
                "message" : "Invalid page"
            })

    def post(self,request):
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def put(self,request):
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def patch(self,request):
        data = request.data
        try:
            obj = Person.objects.get(id=data['id'])
        except Person.DoesNotExist:
            return Response({"error": "Person not found"})
        serializer = PeopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    def delete(self,request):
        data=request.data
        obj=Person.objects.get(id=data["id"])
        obj.delete()
        return Response({"message":"person deleted"})



@api_view(['GET','POST','PUT','PATCH',"DELETE"])
def person(request): 
    if request.method == "GET":
        objs=Person.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(objs, many = True)
        return Response(serializer.data)
    elif request.method == "POST":
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == "PUT":
        data=request.data
        serializer=PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    elif request.method == "PATCH":
        data = request.data
        try:
            obj = Person.objects.get(id=data['id'])
        except Person.DoesNotExist:
            return Response({"error": "Person not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PeopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        data=request.data
        obj=Person.objects.get(id=data["id"])
        obj.delete()
        return Response({"message":"person deleted"})


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class=PeopleSerializer
    queryset=Person.objects.all()

    def list(self, request):
        search=request.GET.get('search')
        queryset=self.queryset
        if search:
            queryset=queryset.filter(name__startswith=search)
        serializer=PeopleSerializer(queryset, many = True)
        return Response({'status' : 200,"data":serializer.data},status=status.HTTP_200_OK)

    @action(detail=True,methods=['POST'])
    def  send_email_to_person(self,request,pk):
        obj=Person.objects.get(pk=pk)
        serializer=PeopleSerializer(obj)
        return Response({
            "status":True,
            "message":"Email sent successfully",
            "data":serializer.data
        })

