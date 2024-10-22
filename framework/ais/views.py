from django.shortcuts import render
from .models import Students
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import StudentsForm
from .models import Students
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from .decorators import group_required
from rest_framework import viewsets
from .serializers import StudentsSerializer
import requests

# Create your views here.
def homepage(request):
    return render(request, 'homepage/index.html')

def about(request):
    return render(request, 'homepage/about.html')

# READ Mahasiswa
def student_index(request):
    query = request.GET.get('q')
    if query:
        response = requests.get(f'http://127.0.0.1:8000/api/students/?search={query}')
    else:
        response = requests.get('http://127.0.0.1:8000/api/students/')
    if response.status_code == 200:
        students = response.json()
    else:
        students = [] # Jika gagal, siapkan list kosong
        return render(request, 'student/index.html', {'students':

Students.objects.all(), 'query': query})

# CREATE Mahasiswa
def student_create(request):
    if request.method == 'POST':
        form_data = {'name': request.POST.get('name'),'nim': request.POST.get('nim'),'email': request.POST.get('email'),'phone_number': request.POST.get('phone_number'),'year': request.POST.get('year'),'teacher': request.POST.get('teacher'),}
        
# Mengirim POST request ke API
        response = requests.post('http://127.0.0.1:8000/api/students/',data=form_data)
        
        if response.status_code == 201:
            messages.success(request, 'Mahasiswa berhasil dibuat!')
            return redirect('student_index')

        else:
            messages.error(request, 'Gagal membuat mahasiswa: ' + response.text)
    else:
        form_data = {}
    return render(request, 'student/create.html', {'form': StudentsForm()})

def student_update(request, student_id):
    if request.method == 'POST':
        form_data = {
                        'name': request.POST.get('name'),
                        'nim': request.POST.get('nim'),
                        'email': request.POST.get('email'),
                        'phone_number': request.POST.get('phone_number'),
                        'year': request.POST.get('year'),
                        'teacher': request.POST.get('teacher'),}
        
# Mengirim PUT request ke API
        response = requests.put(f'http://127.0.0.1:8000/api/students/{student_id}/',data=form_data)

        if response.status_code == 200: # OK
            messages.success(request, 'Data mahasiswa berhasil diubah!')

            return redirect('student_index')
        else:
            messages.error(request, 'Gagal mengubah mahasiswa: ' + response.text)
    else:
        response = requests.get(f'http://127.0.0.1:8000/api/students/{student_id}/')
        if response.status_code == 200:
            student = response.json()
        else:
            return HttpResponseForbidden("Data mahasiswa tidak ditemukan.")
        return render(request, 'student/update.html', {'form': StudentsForm(initial=student), 'student': student})
    
def student_delete(request, student_id):
    if request.method == 'POST':
        response = requests.delete(f'http://127.0.0.1:8000/api/students/{student_id}/')
        
        if response.status_code == 204:

            messages.success(request, 'Data mahasiswa berhasil dihapus')
            return JsonResponse({'success': True})
        else:
            messages.error(request, 'Gagal menghapus mahasiswa: ' + response.text)

            return JsonResponse({'success': False})
    else:
        return HttpResponseForbidden("Metode tidak diizinkan.")

def student_index(request):
    query = request.GET.get('q')
    students = Students.objects.all()
    if query:
        students = Students.objects.filter(
        Q(name__icontains=query) |
        Q(nim__icontains=query) |
        Q(email__icontains=query) |
        Q(phone_number__icontains=query)
    )
    else:
        students = Students.objects.all()
    return render(request, 'student/index.html', {'students': students, 'query': query})


@login_required
def dashboard(request):
    user = request.user
    if user.groups.filter(name='Admin').exists():
        return redirect('dashboard_admin')
    elif user.groups.filter(name='Student').exists():
        return redirect('dashboard_student')
    elif user.groups.filter(name='Teacher').exists():
        return redirect('dashboard_teacher')
    return HttpResponseForbidden("You do not have permission to access this page.")

@login_required
def dashboard_admin(request):
    return render(request, 'dashboard/admin.html')

@login_required
def dashboard_student(request):
    return render(request, 'dashboard/student.html')

@login_required
def dashboard_teacher(request):
    return render(request, 'dashboard/teacher.html')

@group_required('Admin')
def dashboard_admin(request):
    return render(request, 'dashboard/admin.html')

@group_required('Student')
def dashboard_student(request):
    return render(request, 'dashboard/student.html')

@group_required('Teacher')
def dashboard_teacher(request):
    return render(request, 'dashboard/teacher.html')

# API
class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()
    
# API
class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Students.objects.all()