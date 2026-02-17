from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.http import HttpResponse, Http404
from .forms import UploadPDFForm, RegisterForm
from .models import PDF


def index(request):
    if request.user.is_authenticated:
        return redirect('pdf_list')
    return redirect('login')


@login_required
def pdf_list(request):
    pdfs = PDF.objects.filter(user=request.user).order_by('-uploaded_at')
    return render(request, 'pdfs/pdf_list.html', {'pdfs': pdfs})


@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.cleaned_data['file']
            data = f.read()
            pdf = PDF(
                user=request.user,
                filename=f.name,
                content_type=getattr(f, 'content_type', 'application/pdf'),
                data=data,
                size=f.size,
            )
            pdf.save()
            messages.success(request, 'PDF subido correctamente.')
            return redirect('pdf_list')
    else:
        form = UploadPDFForm()
    return render(request, 'pdfs/upload.html', {'form': form})


@login_required
def download_pdf(request, pk):
    pdf = get_object_or_404(PDF, pk=pk)
    if pdf.user != request.user and not request.user.is_staff:
        raise Http404()
    response = HttpResponse(pdf.data, content_type=pdf.content_type)
    response['Content-Disposition'] = f'attachment; filename="{pdf.filename}"'
    return response


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            messages.success(request, 'Cuenta creada y sesión iniciada.')
            return redirect('pdf_list')
    else:
        form = RegisterForm()
    return render(request, 'pdfs/register.html', {'form': form})
