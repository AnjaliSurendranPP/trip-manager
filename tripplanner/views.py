from django.shortcuts import render,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from tripplanner.serializers import UserSerializer,TripSerializer
from django.contrib.auth.models import User
from tripplanner.models import TripDb
from rest_framework import authentication,permissions,serializers
from tripplanner.permissions import OwnerOnly

# Create your views here.
class SignUp(APIView):
    def post(self,request):
        form_data=request.data
        serializer_instance=UserSerializer(data=form_data)

        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={"message":"User created successfully"},status=201)
        else:
            return Response(data=serializer_instance.errors,status=400)

class TripView(APIView):
    authentications_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    def get(self,request):
        qs=TripDb.objects.filter(created_by=request.user)
        serializer_instance=TripSerializer(qs,many=True)
        return Response(data=serializer_instance.data,status=200)

    def post(self,request):
        form_data=request.data
        serializer_instance=TripSerializer(data=form_data)
        created_by=request.user
        if serializer_instance.is_valid():
            serializer_instance.save(created_by=request.user)
            return Response(data={"message":"trip created successfully","trip":serializer_instance.data},status=201)
        else:
            return Response(data=serializer_instance.errors,status=400)

class TripRetrieveUpdateDelete(APIView):
    authentications_classes=[authentication.BasicAuthentication]
    permission_classes=[OwnerOnly]
    def get(self,request,pk):
        trip_object=get_object_or_404(TripDb,id=pk)
        #[1,trip to goa,goa,...]
        serializer_instance=TripSerializer(trip_object)
        return Response(data=serializer_instance.data)

    def put(self,request,pk):
        form_data=request.data
        trip_object=get_object_or_404(TripDb,id=pk)
        serializer_instance=TripSerializer(data=form_data,instance=trip_object)
        if serializer_instance.is_valid():
            serializer_instance.save()
            return Response(data={"message":"trip updated successfully","updated trip":serializer_instance.data},status=201)
        else:
            return Response(serializer_instance.errors)

    def delete(self,request,pk):
        trip_object=get_object_or_404(TripDb,id=pk)
        trip_object.delete()
        return Response(data={"message":f"{request.user} {trip_object.title} deleted successfully"})

    