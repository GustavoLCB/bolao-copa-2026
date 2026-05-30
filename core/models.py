from django.db import models
from django.contrib.auth.models import User

class Partida(models.Model):
    # Nova coluna para agrupar os jogos
    grupo_fase = models.CharField(max_length=50, default="Fase de Grupos")
    
    time_mandante = models.CharField(max_length=50)
    # Nova coluna para a sigla da bandeira do mandante (ex: "br")
    bandeira_mandante = models.CharField(max_length=2, blank=True, null=True)
    
    time_visitante = models.CharField(max_length=50)
    # Nova coluna para a sigla da bandeira do visitante (ex: "ar")
    bandeira_visitante = models.CharField(max_length=2, blank=True, null=True)
    
    data_hora = models.DateTimeField()
    gols_mandante = models.IntegerField(null=True, blank=True)
    gols_visitante = models.IntegerField(null=True, blank=True)
    finalizada = models.BooleanField(default=False)
    
    multiplicador = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.grupo_fase}: {self.time_mandante} x {self.time_visitante}"

    def calcular_pontos(self):
        if not self.finalizada or self.gols_mandante is None or self.gols_visitante is None:
            return

        palpites_deste_jogo = self.palpite_set.all()

        for palpite in palpites_deste_jogo:
            pontos = 0
            gm_real = self.gols_mandante
            gv_real = self.gols_visitante
            gm_palp = palpite.gols_mandante
            gv_palp = palpite.gols_visitante

            saldo_real = gm_real - gv_real
            saldo_palp = gm_palp - gv_palp

            if gm_real == gm_palp and gv_real == gv_palp:
                pontos = 5
            elif saldo_real == 0 and saldo_palp == 0:
                pontos = 2
            elif (saldo_real > 0 and saldo_palp > 0) or (saldo_real < 0 and saldo_palp < 0):
                if saldo_real == saldo_palp:
                    pontos = 3
                elif gm_real == gm_palp or gv_real == gv_palp:
                    pontos = 2
                else:
                    pontos = 1

            palpite.pontos = pontos * self.multiplicador
            palpite.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.calcular_pontos()

class Palpite(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    partida = models.ForeignKey(Partida, on_delete=models.CASCADE)
    gols_mandante = models.IntegerField()
    gols_visitante = models.IntegerField()
    pontos = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.usuario.username} - Placar: {self.gols_mandante}x{self.gols_visitante}"