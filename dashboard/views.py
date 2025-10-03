from django.shortcuts import render
from master.views import master_required
from .models import AntiSpyQuote


@master_required
def dashboard(request):
    quotes = AntiSpyQuote.objects.filter(is_active=True).order_by('-created_at')

    context = {
        'quotes': quotes,
        'master_username': request.session.get('master_username', 'User')
    }
    return render(request, 'dashboard/dashboard.html', context)
