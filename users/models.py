from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# 1. CATÁLOGOS DE CARRERAS
class Career(models.Model):
    name = models.CharField(max_length=150, verbose_name="Nombre de la Carrera")
    plan_key = models.CharField(
        max_length=20, unique=True, verbose_name="Clave del Plan"
    )

    def __str__(self):
        return f"{self.plan_key} - {self.name}"


# 2. PERFILES DE USUARIO
class Coordinator(User):
    class Meta:
        proxy = True  
        verbose_name = 'Coordinador'
        verbose_name_plural = 'Coordinadores'

class StudentProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    # Datos Escolares
    control_number = models.CharField(
        max_length=20, unique=True, verbose_name="Número de Control"
    )
    current_semester = models.PositiveSmallIntegerField(verbose_name="Semestre Actual")

    class Gender(models.TextChoices):
        HOMBRE = "H", "Hombre"
        MUJER = "M", "Mujer"
        OTRO = "O", "Otro"

    gender = models.CharField(
        max_length=1, choices=Gender.choices, verbose_name="Género"
    )

    class StudentType(models.TextChoices):
        INTERNO = "interno", "Interno (Estudiante TEC)"
        EXTERNO = "externo", "Externo / Egresado"

    student_type = models.CharField(
        max_length=10,
        choices=StudentType.choices,
        default=StudentType.INTERNO,
        verbose_name="Tipo de Alumno",
    )

    career = models.ForeignKey(
        Career, on_delete=models.PROTECT, null=True, blank=True, verbose_name="Carrera"
    )
    phone = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Teléfono"
    )

    def __str__(self):
        return f"{self.control_number} - {self.user.get_full_name()}"


class TeacherProfile(models.Model):
    class Category(models.TextChoices):
        CATEGORY_A = "A", "Categoría A"
        CATEGORY_B = "B", "Categoría B"
        CATEGORY_C = "C", "Categoría C"

    class LanguageLevel(models.TextChoices):
        B2 = "B2", "B2"
        C1 = "C1", "C1"
        C2 = "C2", "C2"

    # --- Estatus de Validación ---
    class ValidationStatus(models.TextChoices):
        PENDING = "PENDIENTE", "Pendiente de Revisión"
        APPROVED = "APROBADO", "Validado por Coordinación"
        REJECTED = "RECHAZADO", "Rechazado / Corregir"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_profile",
    )

    validation_status = models.CharField(
        max_length=10,
        choices=ValidationStatus.choices,
        default=ValidationStatus.PENDING,
        verbose_name="Estatus de Validación",
    )

    # --- Motivo de Rechazo ---
    rejection_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name="Motivo de Rechazo",
        help_text="Explica al docente qué documento está mal o qué debe corregir.",
    )

    # --- Datos Generales y Fiscales ---
    category = models.CharField(
        max_length=1, choices=Category.choices, verbose_name="Categoría Solicitada"
    )
    rfc = models.CharField(max_length=13, unique=True, verbose_name="RFC")
    curp = models.CharField(max_length=18, unique=True, verbose_name="CURP")
    bank_name = models.CharField(max_length=50, verbose_name="Banco")
    clabe = models.CharField(max_length=18, verbose_name="CLABE Interbancaria")
    phone = models.CharField(max_length=15, verbose_name="Teléfono")

    # --- Datos Académicos ---
    is_native = models.BooleanField(default=False, verbose_name="¿Es Nativo?")
    language_level = models.CharField(
        max_length=2,
        choices=LanguageLevel.choices,
        blank=True,
        null=True,
        verbose_name="Nivel MCER (Auto-declarado)",
    )

    # --- Campos Condicionales ---
    academic_degree = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Título/Grado"
    )
    ttc_hours = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Horas TTC"
    )
    extra_certificate_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Nombre Certificación Extra (Cat B)",
        help_text="Ej: CELTA, DELTA, ICELT...",
    )

    def __str__(self):
        # Muestra el estatus en el admin
        return (
            f"[{self.validation_status}] {self.user.get_full_name()} ({self.category})"
        )

# 3. EVIDENCIAS
class TeacherEvidence(models.Model):
    class ValidationStatus(models.TextChoices):
        PENDING = "PENDIENTE", "Pendiente"
        APPROVED = "APROBADO", "Aprobado"
        REJECTED = "RECHAZADO", "Rechazado"

    class EvidenceType(models.TextChoices):
        INE = "INE", "Identificación Oficial"
        ACTA = "ACTA", "Acta de Nacimiento"
        CONSTANCIA_FISCAL = "CSF", "Constancia Situación Fiscal"
        TITULO = "TITULO", "Título Profesional"
        TTC_CERT = "TTC", "Constancia TTC"
        TKT_CERT = "TKT", "Certificación TKT"
        CERTIFICACION_EXTRA = "EXTRA", "Certificación Especializada (Cat B)"
        RESIDENCIA = "RES", "Comprobante Residencia (Nativos)"
        ACTUALIZACION = "ACT", "Evidencia de Actualización"

    teacher = models.ForeignKey(
        TeacherProfile, on_delete=models.CASCADE, related_name="evidences"
    )
    evidence_type = models.CharField(max_length=10, choices=EvidenceType.choices)
    file = models.FileField(upload_to="teacher_evidences/%Y/%m/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    validation_status = models.CharField(
        max_length=10,
        choices=ValidationStatus.choices,
        default=ValidationStatus.PENDING,
        verbose_name="Estatus",
    )

    rejection_reason = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Motivo de rechazo",
        help_text="Ej. 'Ilegible', 'Vencido', 'No corresponde'",
    )

    def __str__(self):
        return f"[{self.validation_status}] {self.evidence_type} - {self.teacher.user.username}"


