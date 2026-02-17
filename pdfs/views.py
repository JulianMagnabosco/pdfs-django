from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from .models import PDF
from .serializers import PDFSerializer, PDFUploadSerializer, RegisterSerializer, UserSerializer
from django.contrib.auth.models import User


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(username=username)
            if user.check_password(password):
                token, _ = Token.objects.get_or_create(user=user)
                return Response({
                    'user': UserSerializer(user).data,
                    'token': token.key
                })
            else:
                return Response({'error': 'Credenciales inválidas'}, status=HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=HTTP_404_NOT_FOUND)


class PDFListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pdfs = PDF.objects.filter(user=request.user).order_by('-uploaded_at')
        serializer = PDFSerializer(pdfs, many=True)
        return Response(serializer.data)


class PDFUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PDFUploadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            pdf = serializer.save()
            return Response(PDFSerializer(pdf).data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class PDFDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            pdf = PDF.objects.get(pk=pk)
            if pdf.user != request.user and not request.user.is_staff:
                raise Http404()
            response = FileResponse(pdf.data, content_type=pdf.content_type)
            response['Content-Disposition'] = f'attachment; filename="{pdf.filename}"'
            return response
        except PDF.DoesNotExist:
            return Response({'error': 'PDF no encontrado'}, status=HTTP_404_NOT_FOUND)


class PDFDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            pdf = PDF.objects.get(pk=pk)
            if pdf.user != request.user and not request.user.is_staff:
                raise Http404()
            return Response(PDFSerializer(pdf).data)
        except PDF.DoesNotExist:
            return Response({'error': 'PDF no encontrado'}, status=HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            pdf = PDF.objects.get(pk=pk)
            if pdf.user != request.user and not request.user.is_staff:
                raise Http404()
            pdf.delete()
            return Response({'message': 'PDF eliminado'})
        except PDF.DoesNotExist:
            return Response({'error': 'PDF no encontrado'}, status=HTTP_404_NOT_FOUND)
