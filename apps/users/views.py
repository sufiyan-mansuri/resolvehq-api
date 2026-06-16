from rest_framework import generics, status, permissions
from rest_framework.response import Response
from apps.users.serializers import RegisterSerializer, LoginSerializer, LogoutSerializer

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

# class ProtectedTestAPIView(views.APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         return Response("You are a genuine user", status=status.HTTP_200_OK)
    
# class AdminOnlyAPIView(views.APIView):
#     permission_classes = [permissions.IsAuthenticated, IsAdmin]

#     def get(self, request):
#         return Response("You are an authenticated Admin")

# class AgentOnlyAPIView(views.APIView):
#     permission_classes = [permissions.IsAuthenticated, IsAgent]

#     def get(self, request):
#         return Response("You are an authenticated Agent")
    