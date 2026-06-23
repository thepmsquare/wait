from rest_framework import permissions, viewsets

from .models import WeightEntry
from .serializers import WeightEntrySerializer


class WeightEntryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing weight entries associated with the user.
    """

    serializer_class = WeightEntrySerializer
    permission_classes = [permissions.IsAuthenticated]

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
