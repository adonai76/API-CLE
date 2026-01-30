from rest_framework import serializers
from django.db import transaction
from ..models import TeacherProfile, TeacherEvidence
from .common import UserSerializer, BaseRegistrationSerializer


# SERIALIZER DE DOCENTES
class TeacherRegisterSerializer(BaseRegistrationSerializer):
    user = UserSerializer()

    class Meta:
        model = TeacherProfile
        fields = [
            "user",
            "rfc",
            "curp",
            "category",
            "phone",
            "bank_name",
            "clabe",
            "is_native",
            "language_level",
            "academic_degree",
            "ttc_hours",
            "extra_certificate_name",
        ]

    def validate(self, data):
        """
        Validación específica según la categoría seleccionada.
        """
        category = data.get("category")
        ttc = data.get("ttc_hours")
        degree = data.get("academic_degree")
        extra_cert = data.get("extra_certificate_name")

        # --- REGLA: Categoría A ---
        if category == TeacherProfile.Category.CATEGORY_A:
            if not ttc or ttc < 120:
                raise serializers.ValidationError(
                    {
                        "ttc_hours": "Para Categoría A, se requieren mínimo 120 horas de Teacher Training."
                    }
                )

        # --- REGLA: Categoría B ---
        elif category == TeacherProfile.Category.CATEGORY_B:
            # 1. Horas TTC (150 hrs para B)
            if not ttc or ttc < 150:
                raise serializers.ValidationError(
                    {
                        "ttc_hours": "Para Categoría B, se requieren mínimo 150 horas de Teacher Training."
                    }
                )

            # 2. Nombre del Certificado Extra (Obligatorio para B)
            if not extra_cert:
                raise serializers.ValidationError(
                    {
                        "extra_certificate_name": "Para Categoría B, debes especificar tu certificación (Ej: CELTA, DELTA, TKT Practical)."
                    }
                )

        # --- REGLA: Categoría C ---
        elif category == TeacherProfile.Category.CATEGORY_C:
            if not degree:
                raise serializers.ValidationError(
                    {"academic_degree": "El Grado Académico es obligatorio."}
                )
        return data

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        with transaction.atomic():
            user = self.create_user_with_group(
                user_data=user_data, group_name="Docentes"
            )
            # Creamos el perfil específico
            teacher_profile = TeacherProfile.objects.create(user=user, **validated_data)
        return teacher_profile


class TeacherEvidenceSerializer(serializers.ModelSerializer):
    """
    Se encarga de recibir, validar y guardar los archivos PDF/JPG.
    """

    class Meta:
        model = TeacherEvidence
        fields = [
            "id",  # Útil para que el front sepa qué archivo borrar
            "evidence_type",  # INE, ACTA, TITULO...
            "file",  # El archivo binario
            "validation_status",  # Semáforo (Pendiente/Aprobado/Rechazado)
            "rejection_reason",  # Feedback del coordinador
            "uploaded_at",
        ]
        # El maestro NO debe poder editar su estatus ni escribir su propio feedback.
        read_only_fields = ["validation_status", "rejection_reason", "uploaded_at"]

    def validate_file(self, value):
        """
        Validación de seguridad:
        1. Tamaño máximo (5MB)
        2. Extensiones permitidas (PDF, imágenes)
        """
        limit_mb = 5
        if value.size > limit_mb * 1024 * 1024:
            raise serializers.ValidationError(
                f"El archivo es muy pesado. Máximo {limit_mb}MB."
            )

        # Validar extensión
        if not value.name.lower().endswith((".pdf", ".jpg", ".jpeg", ".png")):
            raise serializers.ValidationError("Formato no válido. Solo PDF, JPG o PNG.")

        return value


class TeacherEvidenceValidationSerializer(serializers.ModelSerializer):
    """
    Serializer exclusivo para COORDINADORES.
    Permite cambiar el estatus de un archivo (Aprobar/Rechazar).
    """

    class Meta:
        model = TeacherEvidence
        fields = ["id", "validation_status", "rejection_reason"]


class TeacherProfileValidationSerializer(serializers.ModelSerializer):
    """
    Serializer exclusivo para COORDINADORES.
    Permite aprobar o rechazar el perfil completo del docente.
    """

    class Meta:
        model = TeacherProfile
        fields = ["id", "validation_status", "rejection_reason"]
