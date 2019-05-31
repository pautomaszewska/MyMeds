from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import date

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .models import Medicine
from .forms import MedicineForm, UserRegisterForm


class MedicineList(LoginRequiredMixin, View):
    def get(self, request):
        today = date.today()
        meds = Medicine.objects.filter(user=request.user).filter(expiration_date__gte=today).order_by('name')
        return render(request, 'medicine.html', {'meds': meds})

    def post(self, request):
        name = request.POST.get('name')
        ingredient = request.POST.get('ingredient')
        try:
            search_name = Medicine.objects.filter(name=name)
            search_ingredient = Medicine.objects.filter(active_ingredient=ingredient)
        except ValueError:
            search_name = None
            search_ingredient = None
        return render(request, 'medicine.html', {'search_name': search_name, 'search_ingredient': search_ingredient})


class AddMedicine(LoginRequiredMixin, View):
    def get(self, request):
        form = MedicineForm()
        return render(request, 'add_medicine.html', {'form': form})

    def post(self, request):
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = Medicine.objects.create(name=form.cleaned_data.get('name'),
                                               active_ingredient=form.cleaned_data.get('active_ingredient'),
                                               amount=form.cleaned_data.get('amount'),
                                               dose=form.cleaned_data.get('dose'),
                                               expiration_date=form.cleaned_data.get('expiration_date'),
                                               user=request.user)
            medicine.save()
            return redirect('medicine')
        else:
            return render(request, 'add_medicine.html', {'form': form})


class DeleteMedicine(LoginRequiredMixin, View):
    def get(self, request, id):
        med = Medicine.objects.get(id=id)
        med.delete()
        return redirect('medicine')


class UpdateMedicine(View):
    def get(self, request, id):
        medicine = Medicine.objects.get(id=id)
        form = MedicineForm(instance=medicine)
        return render(request, 'update_medicine.html', {'form': form, 'med': medicine})

    def post(self, request, id):
        medicine = Medicine.objects.get(id=id)
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect('medicine')


class ExpiredMedicine(LoginRequiredMixin, View):
    def get(self, request):
        today = date.today()
        expired = Medicine.objects.filter(expiration_date__lt=today)
        return render(request, 'expired.html', {'expired': expired})

    def post(self, request):
        name = request.POST.get('name')
        ingredient = request.POST.get('ingredient')
        today = date.today()
        try:
            search_name = Medicine.objects.filter(name=name).filter(expiration_date__lt=today)
            search_ingredient = Medicine.objects.filter(active_ingredient=ingredient).filter(expiration_date__lt=today)
        except ValueError:
            search_name = None
            search_ingredient = None
        return render(request, 'expired.html', {'search_name': search_name, 'search_ingredient': search_ingredient})


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return redirect('login')





