from django.db import models
from django.contrib.auth.models import User


class Participante(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pago = models.BooleanField(default=False)

    total_pontos = models.IntegerField(default=0)
    total_placar_exato = models.IntegerField(default=0)
    total_resultado = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Rodada(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Jogo(models.Model):
    rodada = models.ForeignKey(Rodada, on_delete=models.CASCADE)
    time_casa = models.CharField(max_length=100)
    time_fora = models.CharField(max_length=100)

    gols_casa = models.IntegerField(null=True, blank=True)
    gols_fora = models.IntegerField(null=True, blank=True)

    data_jogo = models.DateTimeField()

    def __str__(self):
        return f"{self.time_casa} x {self.time_fora}"


class Palpite(models.Model):
    participante = models.ForeignKey(Participante, on_delete=models.CASCADE)
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)

    palpite_casa = models.IntegerField()
    palpite_fora = models.IntegerField()

    pontos = models.IntegerField(default=0)

    def calcular_pontos(self):
        if self.jogo.gols_casa is None or self.jogo.gols_fora is None:
            return 0

        # Placar real
        real_casa = self.jogo.gols_casa
        real_fora = self.jogo.gols_fora

        # Placar apostado
        palpite_casa = self.palpite_casa
        palpite_fora = self.palpite_fora

        # 🎯 Regra 1: placar exato
        if real_casa == palpite_casa and real_fora == palpite_fora:
            return 5

        # 🤝 Regra 2: empate
        if real_casa == real_fora and palpite_casa == palpite_fora:
            return 1

        # 🏆 Regra 3: acertar vencedor
        if (real_casa > real_fora and palpite_casa > palpite_fora) or \
           (real_fora > real_casa and palpite_fora > palpite_casa):
            return 3

        return 0

    def __str__(self):
        return f"{self.participante} - {self.jogo}"