from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User

from .models import Medicine
from .forms import MedicineForm


class MedicineList(View):
    def get(self, request):
        meds = Medicine.objects.filter(user=request.user).order_by('name')
        return render(request, 'medicine.html', {'meds': meds})


class AddMedicine(View):
    def get(self, request):
        form = MedicineForm()
        return render(request, 'add_medicine.html', {'form': form})

    def post(self, request):
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
        else:
            return render(request, 'add_medicine.html', {'form': form})
