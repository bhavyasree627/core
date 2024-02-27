from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PeopleSerializer,LoginSerializer
from .models import Person
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
