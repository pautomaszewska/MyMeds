from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect

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


class DeleteMedicine(View):
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
            # medicine = Medicine.objects.get(name=form.cleaned_data.get('name'),
            #                                    active_ingredient=form.cleaned_data.get('active_ingredient'),
            #                                    amount=form.cleaned_data.get('amount'),
            #                                    dose=form.cleaned_data.get('dose'),
            #                                    expiration_date=form.cleaned_data.get('expiration_date'),
            #                                    user=request.user)
            # medicine.name = form.cleaned_data.get('name')
            # medicine.active_ingredient = form.cleaned_data.get('active_ingredient')
            # medicine.amount = form.cleaned_data.get('amount')
            # medicine.dose = form.cleaned_data.get('dose')
            # medicine.expiration_date = form.cleaned_data.get('expiration_date')
            # medicine.save()
            form.save()
            return redirect('medicine')




