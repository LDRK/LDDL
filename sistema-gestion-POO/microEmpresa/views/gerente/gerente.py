from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def gerente_dashboard(request):
    return render(request, 'gerente/dashboardGerente.html')
