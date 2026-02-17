from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings
from .models import PDF


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class PDFSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = PDF
        fields = ('id', 'user', 'filename', 'content_type', 'size', 'uploaded_at')
        read_only_fields = ('user', 'content_type', 'size', 'uploaded_at')


class PDFUploadSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = PDF
        fields = ('file',)

    def validate_file(self, value):
        # Validar tipo de archivo
        content_type = getattr(value, 'content_type', '')
        filename = value.name.lower()
        
        if content_type != 'application/pdf' and not filename.endswith('.pdf'):
            raise serializers.ValidationError('El archivo debe ser un PDF.')
        
        # Validar tamaño máximo
        max_size = settings.MAX_UPLOAD_PDF_SIZE
        if value.size > max_size:
            max_size_mb = max_size / (1024 * 1024)
            raise serializers.ValidationError(
                f'El archivo es demasiado grande. Tamaño máximo: {max_size_mb:.1f}MB'
            )
        
        return value

    def create(self, validated_data):
        file_obj = validated_data['file']
        user = self.context['request'].user
        pdf = PDF(
            user=user,
            filename=file_obj.name,
            content_type=getattr(file_obj, 'content_type', 'application/pdf'),
            data=file_obj.read(),
            size=file_obj.size,
        )
        pdf.save()
        return pdf


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def validate(self, data):
        if data['password'] != data.pop('password2'):
            raise serializers.ValidationError('Las contraseñas no coinciden.')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user
