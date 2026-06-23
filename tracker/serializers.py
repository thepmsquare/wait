from rest_framework import serializers

from .models import WeightEntry


class WeightEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for the WeightEntry model.
    """

    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = WeightEntry
        fields = ["id", "user", "weight", "timestamp"]
        read_only_fields = ["id", "user"]
