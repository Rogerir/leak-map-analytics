import pandas as pd
import os
import random

# Definindo semente para que os dados aleatórios sejam sempre os mesmos
random.seed(42)

estados_info = [
    ('BR-AC', 'Acre'), ('BR-AL', 'Alagoas'), ('BR-AM', 'Amazonas'), ('BR-AP', 'Amapá'),
    ('BR-BA', 'Bahia'), ('BR-CE', 'Ceará'), ('BR-DF', 'Distrito Federal'), ('BR-ES', 'Espírito Santo'),
    ('BR-GO', 'Goiás'), ('BR-MA', 'Maranhão'), ('BR-MG', 'Minas Gerais'), ('BR-MS', 'Mato Grosso do Sul'),
    ('BR-MT', 'Mato Grosso'), ('BR-PA', 'Pará'), ('BR-PB', 'Paraíba'), ('BR-PE', 'Pernambuco'),
    ('BR-PI', 'Piauí'), ('BR-PR', 'Paraná'), ('BR-RJ', 'Rio de Janeiro'), ('BR-RN', 'Rio Grande do Norte'),
    ('BR-RO', 'Rondônia'), ('BR-RR', 'Roraima'), ('BR-RS', 'Rio Grande do Sul'), ('BR-SC', 'Santa Catarina'),
    ('BR-SE', 'Sergipe'), ('BR-SP', 'São Paulo'), ('BR-TO', 'Tocantins')
]

anos = [2018, 2019, 2020, 2021, 2022, 2023]
dados = []

# Gerando dados simulados para cada estado em cada ano
for ano in anos:
    for sigla, nome in estados_info:
        # Lógica simulada: aumento de notificações em 2020/2021 devido à vigência da LGPD
        base_incidentes = random.randint(5, 50)

        if ano in [2020, 2021]:
            incidentes = base_incidentes * random.randint(2, 4)  # Explosão de notificações
        elif ano > 2021:
            incidentes = int(base_incidentes * 1.5)  # Estabilização pós-LGPD
        else:
            incidentes = base_incidentes  # Cenário pré-LGPD (subnotificado)

        volume_gb = incidentes * random.uniform(5.0, 15.0)

        dados.append({
            'Ano': ano,
            'Localidade': sigla,
            'Estado': nome,
            'Incidentes': incidentes,
            'Volume_GB': round(volume_gb, 2)
        })

df = pd.DataFrame(dados)

os.makedirs('data', exist_ok=True)
df.to_csv('data/vazamentos_brasil.csv', index=False)

print("Sucesso! O arquivo 'data/vazamentos_brasil.csv' foi gerado com o histórico anual completo.")