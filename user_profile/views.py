from rest_framework import generics, permissions, status
from rest_framework.response import Response
from user.models import CustomUser
from user.serializers import CustomUserSerializer

class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    API view to retrieve and update the logged-in user's profile.
    """
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """
        Override get_object to return the current user's profile.
        """
        return self.request.user  # Return the logged-in user directly

    def update(self, request, *args, **kwargs):
        """
        Custom update method to handle additional logic.
        """
        # Get the current user object
        user = self.get_object()
        
        # Use the serializer to validate and update the data
        serializer = self.get_serializer(user, data=request.data, partial=True)  # Set partial=True for partial updates
        serializer.is_valid(raise_exception=True)  # Validate the incoming data

        # Save the updated user instance
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)  # Return the updated user data
