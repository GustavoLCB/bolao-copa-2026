import csv
from django.core.management.base import BaseCommand
from core.models import Partida
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware

class Command(BaseCommand):
    help = 'Importa os jogos do arquivo CSV'

    def handle(self, *args, **kwargs):
        caminho_arquivo = 'jogos.csv'
        
        try:
            with open(caminho_arquivo, newline='', encoding='utf-8') as arquivo_csv:
                leitor = csv.DictReader(arquivo_csv)
                
                # Limpa o banco de dados antes de importar
                Partida.objects.all().delete()
                contador = 0
                
                for linha in leitor:
                    data_hora = make_aware(parse_datetime(linha['data_hora']))
                    
                    Partida.objects.create(
                        grupo_fase=linha['grupo_fase'],
                        time_mandante=linha['time_mandante'],
                        bandeira_mandante=linha['bandeira_mandante'],
                        time_visitante=linha['time_visitante'],
                        bandeira_visitante=linha['bandeira_visitante'],
                        data_hora=data_hora,
                        multiplicador=linha['multiplicador']
                    )
                    contador += 1
                    
            self.stdout.write(self.style.SUCCESS(f'Sucesso! {contador} jogos reais foram importados do CSV.'))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Arquivo {caminho_arquivo} não encontrado.'))
        except Exception as erro:
            self.stdout.write(self.style.ERROR(f'Erro na importação: {erro}'))