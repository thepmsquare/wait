from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserSettings, WeightEntry
from .serializers import UserSettingsSerializer, WeightEntrySerializer


class WeightEntryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing weight entries associated with the user.
    """

    serializer_class = WeightEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    # Used by drf-spectacular to infer the integer primary key type.
    queryset = WeightEntry.objects.all()

    def get_queryset(self):
        """
        Filter the weight entries so that the user can only see their own.
        """
        return WeightEntry.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically set the user field to the logged-in user.
        """
        serializer.save(user=self.request.user)


class UserSettingsView(APIView):
    """
    API view to retrieve and update user preferences.
    """

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSettingsSerializer

    def get(self, request):
        user_settings, _ = UserSettings.objects.get_or_create(user=request.user)
        serializer = UserSettingsSerializer(user_settings)
        return Response(serializer.data)

    def put(self, request):
        user_settings, _ = UserSettings.objects.get_or_create(user=request.user)
        serializer = UserSettingsSerializer(
            user_settings, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        return self.put(request)
