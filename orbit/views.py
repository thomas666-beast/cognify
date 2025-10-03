from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from master.views import master_required
from .models import Orbit
from .forms import OrbitForm


@master_required
def orbit_list(request):
    orbits = Orbit.objects.all()

    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter:
        orbits = orbits.filter(status=status_filter)

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        orbits = orbits.search(search_query)

    context = {
        'orbits': orbits,
        'status_choices': Orbit.STATUS_CHOICES,
        'current_status': status_filter,
        'search_query': search_query,
    }
    return render(request, 'orbits/orbit_list.html', context)


@master_required
def orbit_create(request):
    if request.method == 'POST':
        form = OrbitForm(request.POST)
        if form.is_valid():
            orbit = form.save()
            messages.success(request, f'Orbit "{orbit.name}" created successfully!')
            return redirect('orbits:orbit_list')
    else:
        form = OrbitForm()

    context = {
        'form': form,
        'title': 'Create New Orbit'
    }
    return render(request, 'orbits/orbit_form.html', context)


@master_required
def orbit_update(request, slug):
    orbit = get_object_or_404(Orbit, slug=slug)

    if request.method == 'POST':
        form = OrbitForm(request.POST, instance=orbit)
        if form.is_valid():
            orbit = form.save()
            messages.success(request, f'Orbit "{orbit.name}" updated successfully!')
            return redirect('orbits:orbit_list')
    else:
        form = OrbitForm(instance=orbit)

    context = {
        'form': form,
        'orbit': orbit,
        'title': f'Edit Orbit: {orbit.name}'
    }
    return render(request, 'orbits/orbit_form.html', context)


@master_required
def orbit_delete(request, slug):
    orbit = get_object_or_404(Orbit, slug=slug)

    if request.method == 'POST':
        orbit_name = orbit.name
        orbit.delete()
        messages.success(request, f'Orbit "{orbit_name}" deleted successfully!')
        return redirect('orbits:orbit_list')

    context = {
        'orbit': orbit
    }
    return render(request, 'orbits/orbit_confirm_delete.html', context)


@master_required
def orbit_detail(request, slug):
    orbit = get_object_or_404(Orbit, slug=slug)

    context = {
        'orbit': orbit
    }
    return render(request, 'orbits/orbit_detail.html', context)


@master_required
def orbit_activate(request, slug):
    orbit = get_object_or_404(Orbit, slug=slug)
    orbit.activate()
    messages.success(request, f'Orbit "{orbit.name}" activated successfully!')
    return redirect('orbits:orbit_list')


@master_required
def orbit_deactivate(request, slug):
    orbit = get_object_or_404(Orbit, slug=slug)
    orbit.deactivate()
    messages.success(request, f'Orbit "{orbit.name}" deactivated successfully!')
    return redirect('orbits:orbit_list')


@master_required
def orbit_archive(request, slug):
    orbit = get_object_or_404(Orbit, slug=slug)
    orbit.archive()
    messages.success(request, f'Orbit "{orbit.name}" archived successfully!')
    return redirect('orbits:orbit_list')
