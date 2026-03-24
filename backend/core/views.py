from django.shortcuts import render
from .models import Participante


def ranking(request):
    participantes = Participante.objects.all().order_by(
        '-total_pontos',
        '-total_placar_exato',
        '-total_resultado'
    )

    return render(request, 'ranking.html', {'participantes': participantes})