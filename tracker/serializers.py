from decimal import Decimal
from rest_framework import serializers

from .models import WeightEntry, UserSettings


class WeightEntrySerializer(serializers.ModelSerializer):
    """
    Serializer for the WeightEntry model.
    """

    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = WeightEntry
        fields = ["id", "user", "weight", "unit", "timestamp"]
        read_only_fields = ["id", "user"]


class UserSettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for the UserSettings model.
    Converts target_weight to/from preferred unit on output/input.
    """

    class Meta:
        model = UserSettings
        fields = ["target_weight", "preferred_unit"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # If preferred unit is lb, convert target_weight from kg to lb
        if instance.preferred_unit == "lb":
            lb_val = Decimal(instance.target_weight) / Decimal("0.45359237")
            ret["target_weight"] = f"{round(lb_val, 2):.2f}"
        else:
            ret["target_weight"] = f"{round(instance.target_weight, 2):.2f}"
        return ret

    def validate(self, attrs):
        preferred_unit = attrs.get("preferred_unit", self.instance.preferred_unit if self.instance else "kg")
        if "target_weight" in attrs:
            target_weight = attrs["target_weight"]
            if preferred_unit == "lb":
                # Convert target_weight in lb to kg for DB storage
                attrs["target_weight"] = round(target_weight * Decimal("0.45359237"), 2)
        return attrs

