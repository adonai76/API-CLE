from .common import BaseRegistrationSerializer
from ..models import Coordinator

# SERIALIZER DE COORDINADORES
class CoordinatorRegisterSerializer(BaseRegistrationSerializer):
    class Meta:
        model = Coordinator
        fields = ["username", "password", "email", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}, "email": {"required": True}}

    def create(self, validated_data):
        user = self.create_user_with_group(
            user_data=validated_data,
            group_name="Coordinadores",
            is_staff=True,  # <--- Coordinadores son staff
        )
        return user
