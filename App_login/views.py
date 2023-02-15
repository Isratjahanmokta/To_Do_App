from App_login.models import Task,UserSignUp
from .serializers import TaskSerializer, userSerializers, LogoutSerializer
from rest_framework import generics, parsers
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import permission_classes

# Create your views here.
class SignUp(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    queryset = UserSignUp.objects.all()
    serializer_class = userSerializers
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    serializer_class = LogoutSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.user)
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
@permission_classes([IsAuthenticated])
class TaskList(generics.ListAPIView):
    search_fields = ['^title']
    filter_backends = (filters.SearchFilter,)
    serializer_class = TaskSerializer
    
    def get_queryset(self):
        task = Task.objects.filter(user=self.request.user)
        return task

class TaskCreate(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
     
class TaskDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer 
    lookup_field = 'id'

class TaskUpdate(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer 
    lookup_field = 'id'

class TaskDelete(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Task.objects.all()
    serializer_class = TaskSerializer 
    lookup_field = 'id'