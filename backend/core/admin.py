from django.contrib import admin
from .models import Participante, Rodada, Jogo, Palpite

admin.site.register(Participante)
admin.site.register(Rodada)
admin.site.register(Jogo)
admin.site.register(Palpite)