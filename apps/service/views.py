from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Branch, Complaint
from .forms import ComplaintForm
from apps.catalog.models import Product


def branches_view(request):
    branches = Branch.objects.all()
    return render(request, 'service/branches.html', {'branches': branches})


def complain_view(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save()
            messages.success(
                request,
                f'Thank you, {complaint.name}. Your support ticket #{complaint.id} has been registered. Our RMA service engineers will contact you shortly.'
            )
            return redirect('service:complain')
    else:
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
                'phone': request.user.phone,
            }
        form = ComplaintForm(initial=initial_data)

    return render(request, 'service/complain.html', {'form': form})


def brands_view(request):
    return redirect('catalog:brand_list')

