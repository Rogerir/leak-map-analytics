import pandas as pd
import os

dados_vazamentos = {
    'Localidade': ['BR-AC', 'BR-AL', 'BR-AM', 'BR-AP', 'BR-BA', 'BR-CE', 'BR-DF', 'BR-ES', 'BR-GO', 'BR-MA',
                   'BR-MG', 'BR-MS', 'BR-MT', 'BR-PA', 'BR-PB', 'BR-PE', 'BR-PI', 'BR-PR', 'BR-RJ', 'BR-RN',
                   'BR-RO', 'BR-RR', 'BR-RS', 'BR-SC', 'BR-SE', 'BR-SP', 'BR-TO'],
    'Estado': ['Acre', 'Alagoas', 'Amazonas', 'Amapá', 'Bahia', 'Ceará', 'Distrito Federal', 'Espírito Santo',
               'Goiás', 'Maranhão', 'Minas Gerais', 'Mato Grosso do Sul', 'Mato Grosso', 'Pará', 'Paraíba',
               'Pernambuco', 'Piauí', 'Paraná', 'Rio de Janeiro', 'Rio Grande do Norte', 'Rondônia', 'Roraima',
               'Rio Grande do Sul', 'Santa Catarina', 'Sergipe', 'São Paulo', 'Tocantins'],
    'Incidentes': [12, 25, 45, 8, 110, 95, 150, 40, 55, 30, 180, 22, 35, 50, 28, 85, 20, 140, 290, 32, 15, 7, 130, 115, 18, 450, 14],
    'Volume_GB': [50, 120, 310, 30, 950, 820, 1500, 280, 410, 190, 1800, 160, 240, 380, 210, 750, 110, 1400, 3200, 240, 80, 25, 1200, 1100, 130, 5800, 70]
}


df = pd.DataFrame(dados_vazamentos)


os.makedirs('data', exist_ok=True)

df.to_csv('data/vazamentos_brasil.csv', index=False)

print("Sucesso! O arquivo 'data/vazamentos_brasil.csv' foi gerado corretamente.")