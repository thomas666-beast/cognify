from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from master.views import master_required
from .models import Participant
from .forms import ParticipantForm


@master_required
def participant_list(request):
    participants = Participant.objects.all()

    # Filter by position if provided
    position_filter = request.GET.get('position')
    if position_filter:
        participants = participants.filter(position=position_filter)

    # Filter by status if provided
    status_filter = request.GET.get('status')
    if status_filter == 'active':
        participants = participants.filter(is_active=True)
    elif status_filter == 'inactive':
        participants = participants.filter(is_active=False)

    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        participants = participants.search(search_query)

    context = {
        'participants': participants,
        'position_choices': Participant.POSITION_CHOICES,
        'current_position': position_filter,
        'current_status': status_filter,
        'search_query': search_query,
    }
    return render(request, 'participants/participant_list.html', context)


@master_required
def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            messages.success(request, f'Participant "{participant.display_name}" created successfully!')
            return redirect('participants:participant_list')
    else:
        form = ParticipantForm()

    context = {
        'form': form,
        'title': 'Add New Participant'
    }
    return render(request, 'participants/participant_form.html', context)


@master_required
def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)

    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            participant = form.save()
            messages.success(request, f'Participant "{participant.display_name}" updated successfully!')
            return redirect('participants:participant_list')
    else:
        form = ParticipantForm(instance=participant)

    context = {
        'form': form,
        'participant': participant,
        'title': f'Edit Participant: {participant.display_name}'
    }
    return render(request, 'participants/participant_form.html', context)


@master_required
def participant_detail(request, pk):
    participant = get_object_or_404(Participant, pk=pk)

    context = {
        'participant': participant
    }
    return render(request, 'participants/participant_detail.html', context)


@master_required
def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)

    if request.method == 'POST':
        participant_name = participant.display_name
        participant.delete()
        messages.success(request, f'Participant "{participant_name}" deleted successfully!')
        return redirect('participants:participant_list')

    context = {
        'participant': participant
    }
    return render(request, 'participants/participant_confirm_delete.html', context)


@master_required
def participant_activate(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    participant.activate()
    messages.success(request, f'Participant "{participant.display_name}" activated successfully!')
    return redirect('participants:participant_list')


@master_required
def participant_deactivate(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    participant.deactivate()
    messages.success(request, f'Participant "{participant.display_name}" deactivated successfully!')
    return redirect('participants:participant_list')
