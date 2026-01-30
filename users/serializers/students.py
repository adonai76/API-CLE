from django.db import transaction
from ..models import StudentProfile
from .common import UserSerializer, BaseRegistrationSerializer


# SERIALIZER DE ALUMNOS
class StudentRegisterSerializer(BaseRegistrationSerializer):
    user = UserSerializer()

    class Meta:
        model = StudentProfile
        fields = [
            "user",
            "control_number",
            "current_semester",
            "gender",
            "student_type",
            "career",
            "phone",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        with transaction.atomic():
            user = self.create_user_with_group(
                user_data=user_data, group_name="Alumnos"
            )

            student_profile = StudentProfile.objects.create(user=user, **validated_data)
        return student_profile
