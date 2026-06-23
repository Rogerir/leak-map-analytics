# O Futuro dos Empregos com a IA (Dashboard)

Um dashboard analítico e interativo desenvolvido em Python com foco em analisar o impacto da Inteligência Artificial no mercado de trabalho até 2030. O painel responde a perguntas cruciais: quais profissões sobrevivem, quanto pagam e o que precisamos aprender para nos mantermos relevantes?

## Funcionalidades

O projeto adota uma abordagem de *Storytelling de Dados*, dividido em três "Atos" principais, e conta com os seguintes recursos:

*   **Filtro Dinâmico:** Análise segmentada por Área de Atuação (Indústria).
*   **Integração de API:** Conversão da média salarial anual de Dólar (USD) para Real (BRL) em tempo real usando a API da AwesomeAPI.
*   **KPIs em Tempo Real:** Cards indicando o total de cargos analisados, risco médio de automação do setor e a média salarial.
*   **Ato 1 (Dispersão):** Gráfico que cruza o "Risco da IA roubar a vaga" com o "Crescimento de Vagas", dimensionado pelo salário.
*   **Ato 2 (Top Jobs):** Gráfico de barras horizontais destacando os 5 cargos com maior potencial de contratação futura.
*   **Ato 3 (Habilidades):** Gráfico de barras mapeando as 5 habilidades técnicas mais exigidas pelas empresas.
*   **Alerta de Estudos Inteligente:** Um painel lateral que avisa o usuário se o setor selecionado exige atualização urgente ou se a situação está controlada.
*   **Dark/Light Mode:** Botão interativo para alternar o tema visual de todo o painel, garantindo melhor acessibilidade e UX.

## Tecnologias Utilizadas

*   **Python:** Linguagem base do projeto.
*   **Dash (by Plotly):** Framework web para a construção da interface do dashboard.
*   **Plotly Express:** Biblioteca para a criação dos gráficos interativos.
*   **Pandas:** Manipulação, limpeza e agregação dos dados do arquivo CSV.
*   **Requests:** Consumo de API externa para cotação de moedas.

## Estrutura do Projeto

\`\`\`text
leak-map-analytics/
├── data/
│   └── AI_Impact_on_Jobs_2030.csv
├── app.py
├── requirements.txt
└── README.md
\`\`\`

## Como Executar o Projeto Localmente

1. **Clone o repositório:**
   \`\`\`bash
   git clone https://github.com/Rogerir/leak-map-analytics.git
   \`\`\`

2. **Acesse a pasta do projeto:**
   \`\`\`bash
   cd seu-repositorio
   \`\`\`

3. **Crie um ambiente virtual (Opcional, mas recomendado):**
   \`\`\`bash
   python -m venv .venv
   source .venv/bin/activate  # No Linux/Mac
   .venv\Scripts\activate     # No Windows
   \`\`\`

4. **Instale as dependências:**
   \`\`\`bash
   pip install dash pandas plotly requests
   \`\`\`

5. **Execute a aplicação:**
   \`\`\`bash
   python app.py
   \`\`\`

6. **Acesse no navegador:**
   Abra o endereço \`http://127.0.0.1:8050\` no seu navegador padrão.

---
*Projeto desenvolvido para fins de análise de dados e estudo do impacto tecnológico no mercado de trabalho.*

```
